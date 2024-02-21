from django.urls import reverse
from django.conf import settings

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.postgres.fields import ArrayField
from django_quill.fields import QuillField
from django.db.models import Avg, Sum
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from base64 import b64encode
from django.utils.text import slugify
from cart.models import Cart

# Create your models here.
user = get_user_model()
ORDER_STATUS = (('pending', 'Pending'),('cancelled', 'Cancelled'),('confirmed', 'Confirmed'),('delivered', 'Delivered'),('failed to delivered', 'Failed To Delivered'),('out for delivery', 'Out for delivery'),('returned', 'Returned'),('refunded', 'Refunded'),('refund requested','Refund Requested'))

class SellerOrder(models.Model):
    order_id = models.CharField(_("Order Id"), max_length=50,primary_key=True)
    order_date = models.DateTimeField(_("Order Date"), auto_now=False, auto_now_add=False)
    customer_id = models.ForeignKey(user, verbose_name=_("User"), on_delete=models.CASCADE,default="")
    billing_address = models.TextField(_("Billing Address"), max_length=1000,default="")
    shipping_address = models.TextField(_("Shipping Address"), max_length=1000,default="")
    order_item = models.ForeignKey(Cart, verbose_name=_("Order Item"), on_delete=models.CASCADE,default="")
    order_status = models.CharField(_("Order Status"), max_length=50,choices=ORDER_STATUS)
    created_at = models.DateTimeField(_("Order Created at"), auto_now=True, auto_now_add=False)
    
    class Meta:
        verbose_name = _("SellerOrder")
        verbose_name_plural = _("SellerOrders")

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse("SellerOrder_detail", kwargs={"pk": self.pk})

