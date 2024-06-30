from django.db import models
from django.conf import settings
from stores.models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import date
import decimal
from math import ceil


User = get_user_model()

STATUS =(('Shipped','SHIPPED'),('Ordered','ORDERED'),('In-transit','IN TRANSIT'),('Out-For-Delivery','OUT FOR DELIVERY'),('Delivered','DELIVERED'),('Refund Requested','REFUND REQUESTED'),('Refunded','REFUNDED'))

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,null=True,blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    size = models.CharField(_("Item Size"), max_length=50,
                            null=True, blank=True, default="L")
    created_at = models.DateTimeField(_("Created Date"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified Date"), auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Cart'

    def __str__(self):
        return f"{self.quantity} Size:{self.size} of {self.item.name}"

    def get_total_item_price(self):
        return ceil(self.quantity * self.item.max_retail_price)

    def get_total_discount_item_price(self):
        return ceil(self.quantity * ((self.item.discount/100)*self.item.max_retail_price))

    def get_amount_saved(self):
        return ceil(self.get_total_item_price() - self.get_total_discount_item_price())
    
    def amount_after_applying_discount(self):
        return ceil(self.get_total_item_price() - self.get_total_discount_item_price())

    def get_final_price(self):
        if self.item.discount:
            return ceil(self.amount_after_applying_discount())
        return ceil(self.get_total_item_price())
    
    def get_product_name(self):
        return self.item.name


class DeliveryPartnerDetails(models.Model):
    name = models.CharField(_("Courier Partner Name"), max_length=50)
    address = models.CharField(_("Courier Partner Address"), max_length=2000)
    contact_no = models.CharField(
        _("Courier Partner Contact No"), max_length=50)
    customer_care = models.CharField(
        _("Courier Partner Customer Care"), max_length=50)
    toll_free_number = models.CharField(
        _("Courier Partner Toll Free Number"), max_length=50)
    email = models.EmailField(_("Courier Partner Email"), max_length=254)

    def __str__(self) -> str:
        return f"Name: {self.name} Ph. No: {self.contact_no}"


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,null=True,blank=True)
    ref_code = models.CharField(max_length=200, blank=True, null=True)
    tracking_id = models.CharField(max_length=200, blank=True, null=True)
    items = models.ManyToManyField(Cart)
    start_date = models.DateTimeField(auto_now_add=True,verbose_name="Addition to cart date")
    shipping_address = models.CharField(_("shipping_address"), max_length=250,blank=True,null=True)
    billing_address = models.CharField(_("billing_address"), max_length=250,blank=True,null=True)
    orderNote = models.CharField(
        _("Order Note"), max_length=250, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(
        _("Order Status"), max_length=255, choices=STATUS, null=True, blank=True, default="ordered")
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    
    shipped = models.BooleanField(default=False)
    shipped_date = models.DateTimeField(
        auto_now_add=True)

    shipping_by = models.ForeignKey(DeliveryPartnerDetails, verbose_name=_("Delivery Partner"), on_delete=models.CASCADE,blank=True,null=True)
    
    out_for_delivery = models.BooleanField(default=False)
    out_for_delivery_date = models.DateTimeField(
        auto_now_add=True)
    
    delivered = models.BooleanField(default=False)
    delivered_date = models.DateTimeField(
        auto_now_add=True)

    refund_requested = models.BooleanField(default=False)
    refund_requested_date = models.DateTimeField(
        auto_now_add=True)

    refund_granted = models.BooleanField(default=False)
    refund_granted_date = models.DateTimeField(
        auto_now_add=True)
    
    refund_request_cancelled = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(_("Razorpay Order id"), max_length=500,null=True,blank=True)
    razorpay_payment_id = models.CharField(_("Razorpay Payment id"), max_length=500,null=True,blank=True)
    razorpay_payment_signature = models.CharField(_("Razorpay Payment Signature"), max_length=500,null=True,blank=True)

    phonepe_id = models.CharField(_("PhonePe Payment Id"), max_length=100,null=True,blank=True)
    phonepe_merchant_transaction_id = models.CharField(_("PhonePe Transaction Id"),max_length=36,null=True,blank=True)


    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''
    @property
    def sid(self):
        return "VAMS/{}/{}".format(date.today().strftime("%Y/%m%d"),self.id)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return ceil(total)
    
    def get_max_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return ceil(total)
    
    def get_order_name(self):
        name = ''
        for order_item in self.items.all():
            name = order_item.get_product_name()
        return name
    
    def get_total_items_in_order(self):
        return len(self.items.all()) - 1
    
    def get_quantity(self):
        qty = 0
        for order_item in self.items.all():
            qty += order_item.quantity

        return qty
    
    def get_total_discount(self):
        return self.get_max_total() - self.get_total()
    
    def shipping_charge(self):
        amount = self.get_total()

        if amount > settings.ABOVE_AMOUNT:
            return 0
        return 40

    
    def amount_with_shipping(self):
        amount = self.get_total()

        if amount > settings.ABOVE_AMOUNT:
            amount += settings.DELIVERY
        return ceil(amount)
    
    def gst_amount(self):
        gst_amount = (float(self.amount_with_shipping()) * (settings.GST_STICHED/100))
        return ceil(gst_amount)

    
    def total_amount_at_checkout(self):
        total_amount = float(self.amount_with_shipping()) + self.gst_amount()
        return ceil(total_amount)
    


    
class Payment(models.Model):
    instamojo_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class PhonePePaymentRequestDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.ForeignKey(Order, verbose_name=_("Order id"), on_delete=models.CASCADE,blank=True,null=True)
    amount = models.CharField(_("amount"), max_length=50,null=True,blank=True)
    success = models.BooleanField(_("Success"),default=False)
    code = models.CharField(_("Code"), max_length=50, blank=True, null=True)
    message = models.TextField(_("Message"))
    merchant_transaction_id = models.CharField(_("Merchant Transaction Id"), max_length=200,null=True, blank=True)
    transaction_id = models.CharField(_("Transaction Id"), max_length=200,null=True, blank=True)
    redirect_url = models.TextField(_("URL"))
    created_at = models.DateTimeField(_("created at"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("PhonePePaymentRequestDetail")
        verbose_name_plural = _("PhonePePaymentRequestDetails")

    def __str__(self):
        return "Order Id: "

    def get_absolute_url(self):
        return reverse("PhonePePaymentDetail_detail", kwargs={"pk": self.pk})
    
    def get_order_sid(self):
        return self.order_id.sid

class PhonePePaymentCallbackDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.ForeignKey(Order, verbose_name=_("Order id"), on_delete=models.CASCADE,blank=True,null=True)
    amount = models.CharField(_("amount"), max_length=50,null=True,blank=True)
    code = models.CharField(_("Code"), max_length=50, blank=True, null=True)

    merchant_transaction_id = models.CharField(_("Transaction Id"), max_length=200,null=True, blank=True)
    provider_reference_id = models.CharField(_("Provider Reference Id"), max_length=200,null=True,blank=True)
    checksum = models.TextField(_("checksum"))


    

    class Meta:
        verbose_name = _("PhonePePaymentCallbackDetail")
        verbose_name_plural = _("PhonePePaymentCallbackDetails")

    def __str__(self):
        return "Order Id: "

    def get_absolute_url(self):
        return reverse("PhonePePaymentCallbackDetail_detail", kwargs={"pk": self.pk})
    
    def get_order_sid(self):
        return self.order_id.sid




class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class UserBankAccount(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE,null=True,blank=True)
    bank_account_number = models.CharField(_("Bank Account No."), max_length=100)
    ifsc_code = models.CharField(_("IFSC Code"), max_length=50)
    account_name = models.CharField(_("Account Holder Name"), max_length=250,null=True,blank=True)
    nick_name = models.CharField(_("Nick Name"), max_length=50,null=True,blank=True)

    

    class Meta:
        verbose_name = _("UserBankAccount")
        verbose_name_plural = _("UserBankAccounts")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("UserBankAccount_detail", kwargs={"pk": self.pk})


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True,blank=True)
    order_sid = models.CharField(_("Order Reference Id"), max_length=50,default="")
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    refund_bank_account = models.ForeignKey(UserBankAccount, verbose_name=_("Refund Bank Account"), on_delete=models.CASCADE,default="")

    def __str__(self):
        return f"{self.pk}"


class PendingPayment(models.Model):
    order_id = models.CharField(
        _("Order ID"), max_length=250, default="", null=True, blank=True)
    order_payment_id = models.CharField(
        _("Payment ID"), max_length=250, default="", null=True, blank=True)
    phone = models.CharField(_("Buyer Phone Number"),
                             max_length=50, default="", null=True, blank=True)
    email = models.EmailField(
        _("Buyer Email"), max_length=254, default="", null=True, blank=True)
    buyer_name = models.CharField(
        _("Buyer Name"), max_length=250, default="", null=True, blank=True)
    amount = models.FloatField()
    purpose = models.CharField(
        _("Buyer Payment Purpose"), max_length=250, default="", null=True, blank=True)
    status = models.CharField(
        _("Payment Status"), max_length=50, default="", null=True, blank=True)
    api_response = models.CharField(
        _("Payment API Response"), max_length=5000, default="", null=True, blank=True)
    created_at = models.CharField(
        _("Payment Created At"), max_length=50, default="", null=True, blank=True)
    modified_at = models.CharField(
        _("Payment Modified At"), max_length=50, default="", null=True, blank=True)

    def __str__(self):
        return self.order_id

