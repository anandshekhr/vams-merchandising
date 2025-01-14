# from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import (
    render,
    redirect,
    HttpResponse,
    get_list_or_404,
    get_object_or_404,
)
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth, messages
from rest_framework import generics, status, authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Products
from .models import *
from .serializers import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from stores.models import *
from wishlist.models import *
from Home.views import get_meta_data
from user.models import UserAddresses
from instamojo_wrapper import Instamojo
import requests
import razorpay
import uuid
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env
from django.views.decorators.csrf import csrf_protect,csrf_exempt

s2s_callback_url = settings.PAYMENT_SUCCESS_REDIRECT_URL
id_assigned_to_user_by_merchant = settings.PHONEPE_USER_ID

api = Instamojo(
    api_key=settings.API_KEY,
    auth_token=settings.AUTH_TOKEN,
    endpoint="https://test.instamojo.com/api/1.1/",
)

razorpay_api = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_KEY_SECRET)
)


merchant_id = settings.PHONEPE_MERCHANT_ID
salt_key = settings.PHONEPE_SALT_KEY
salt_index = 1
env = Env.UAT  # Change to Env.PROD when you go live

phonepe_client = PhonePePaymentClient(
    merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env
)

User = get_user_model()


@login_required(login_url="login")
def cartCheckoutPageView(request):
    counter = 0
    a = 0
    b = 0
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())
    try:
        if request.user:
            itemsForCartPage = Order.objects.get(user=request.user.id, ordered=False)

        a = ceil(itemsForCartPage.get_total())
        counter = len(itemsForCartPage.items.all())

        if a > 599:
            delivery_charges = 0
        else:
            delivery_charges = 40

        grandtotal = a + delivery_charges

        context = {
            "object": itemsForCartPage,
            "delivery": ceil(delivery_charges),
            "totalquantity": counter,
            "grandtotal": ceil(grandtotal),
            "page_title": title,
            "description": desc,
            "keyword": key,
            "canonical": canonical,
        }
    except Order.DoesNotExist:
        context = {
            "object": 0,
            "delivery": 0,
            "totalquantity": 0,
            "grandtotal": 0,
            "page_title": title,
            "description": desc,
            "keyword": key,
            "canonical": canonical,
        }

    return render(request, "cart/cart.html", context)


@login_required(login_url="login")
def addToCart(request, pk, size):
    item = get_object_or_404(Products, id=pk)
    order_item, created = Cart.objects.get_or_create(
        item=item, size=size, user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id, size="L").exists() and item.stock > 0:
            order_item.quantity += 1
            item.stock = item.stock - 1
            item.save()
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cartview")

        elif item.stock > 0:
            order.items.add(order_item)
            item.stock = item.stock - 1
            item.save()
            messages.info(request, "This item was added to your cart.")
            return redirect("cartview")

        else:
            messages.info(request, "Item Out of Stock")
            return redirect("/")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cartview")


class moveToCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        pk = request.data.get("id")

        size = request.data.get("size")

        # delete from wishlistItems models
        iitem = WishlistItems.objects.filter(item=pk)[0]
        iitem.delete()

        # delete from Wishlist models
        wishlist_item = Wishlist.objects.filter(user=request.user)[0]
        wishlist_item.items.remove(iitem)

        item = get_object_or_404(Products, id=pk)
        order_item, created = Cart.objects.get_or_create(
            item=item, size=size, user=request.user, ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__id=item.id).exists() and item.stock > 0:
                order_item.quantity += 1
                item.stock = item.stock - 1
                item.save()
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return Response({"status": "Item Updated"}, status=status.HTTP_200_OK)

            elif item.stock > 0:
                order.items.add(order_item)
                item.stock = item.stock - 1
                item.save()
                messages.info(request, "This item was added to your cart.")
                return Response({"status": "Item Updated"}, status=status.HTTP_200_OK)

            else:
                messages.info(request, "Item Out of Stock")
                return Response(
                    {"status": "Item Out of Stock"}, status=status.HTTP_403_FORBIDDEN
                )

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return Response(
                {"status": "Item Out of Stock"}, status=status.HTTP_403_FORBIDDEN
            )

@csrf_exempt
def PhonePePaymentCallbackAPI(request):
    if request.method == "POST":
        status  = request.POST.get('code')
        if status == 'PAYMENT_SUCCESS':
            print(request.POST.dict())
            transaction_id = request.POST.get('transactionId')
            order = Order.objects.get(phonepe_merchant_transaction_id=transaction_id, ordered=False)

            print("Order: ",order)
            order.ref_code = request.POST.get('providerReferenceId')
            order.ordered = True
            order.status = "ordered"
            order.ordered_date = datetime.now()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()
            
            payment_success_details = PhonePePaymentCallbackDetail()
            payment_success_details.user = order.user
            payment_success_details.order_id = order
            payment_success_details.amount = str(int(request.POST.get('amount'))/100)
            payment_success_details.code = status
            payment_success_details.merchant_transaction_id = request.POST.get('transactionId')
            payment_success_details.provider_reference_id = request.POST.get('providerReferenceId')
            payment_success_details.checksum = request.POST.get('checksum')
            payment_success_details.save()
            order.phonepe_id = payment_success_details.pk
            order.save()

            # for item in order_items:
            #     # Vendor Order Details
            #     vender_order = VendorOrderDetail()
            #     vender_order.vendor = item.item.vendor

            #     vender_order.order_id = order.sid
            #     product_id = Products.objects.get(id=item.item.id)
            #     vender_order.order_item = product_id
            #     vender_order.order_item_size = item.size
            #     vender_order.order_item_qty = item.quantity
            #     vender_order.order_amount = item.get_final_price()
            #     vender_order.delivery_address = order.shipping_address
            #     vender_order.payment_status = "Paid"
            #     vender_order.save()

            #     # vendor transaction detail
            #     (
            #         vender_transaction,
            #         created,
            #     ) = VendorTransactionDetail.objects.get_or_create(
            #         vendor=item.item.vendor,
            #         order_id=order.sid,
            #     )
            #     if created:
            #         vender_transaction.total_order_amount = item.get_final_price()
            #         vender_transaction.order_receiving_date = datetime.now()
            #         vender_transaction.save()

            #     else:
            #         vender_transaction.total_order_amount += item.get_final_price()
            #         vender_transaction.save()
        
    return redirect('payment-status-update-phonepe')



def deleteItemFromCart(request, pk):
    """Delete Items from Wishlist

    Args:
        request (_type_): _description_
        pk (int): product ID

    Returns:
        _type_: _description_
    """
    current_site = get_current_site(request)
    domain_name = request.get_host()

    previous_page = request.META.get("HTTP_REFERER")

    # delete from wishlistItems models
    item = Cart.objects.filter(item=pk, user=request.user, ordered=False)[0]
    item.delete()

    # delete from Wishlist models
    cart_item = Order.objects.filter(user=request.user, ordered=False)[0]
    cart_item.items.remove(item)

    return redirect(previous_page)


@login_required(login_url="login")
def removeSingleItemFromCart(request, pk):
    if request.user:
        user_details = UserAddresses.objects.get(user=request.user.id)
    item = get_object_or_404(
        StoreProductsDetails,
        products=pk,
        store__storeServicablePinCodes__contains=[user_details.pincode],
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__products__id=item.products.id).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                item.available_stock += 1
                item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
                item.available_stock += 1
                item.save()
            # messages.info(request, "This item quantity was updated.")
            return redirect("cartview")
        else:
            # messages.info(request, "This item was not in your cart")
            return redirect("/")
    else:
        # messages.info(request, "You do not have an active order")
        return redirect("/")


@login_required(login_url="login")
def orderPaymentRequestInstamojo(request, amount):
    """Request for Order Payment using Instamojo Payment Gateway

    Args:
        amount (int): request amount to be collected
    """

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        order = Order.objects.get(user=request.user.id, ordered=False)

        if request.method == "POST":
            firstName = request.POST.get("first_name")
            lastName = request.POST.get("last_name")
            area = (
                request.POST.get("address_line_1")
                + ","
                + request.POST.get("address_line_2")
            )
            country = request.POST.get("country")
            city = request.POST.get("city")
            state = request.POST.get("state")
            pincode = request.POST.get("pincode")
            email = request.POST.get("email")
            phoneNumber = request.POST.get("phone_number")

            ifSaveAddress = request.POST.get("save-address")
            ifShipToDifferentAddress = request.POST.get("ship-box")

            BillingAddress = (
                "Name: "
                + firstName
                + " "
                + lastName
                + ",\n Address: "
                + area
                + ", "
                + city
                + ", "
                + state
                + ", "
                + country
                + ",\n Pincode: "
                + pincode
                + ",\n Email: "
                + email
                + ",\n Ph: "
                + phoneNumber
                or None
            )

            if (
                pincode != None
                or area != None
                or country != None
                or city != None
                or state != None
            ):
                order.billing_address = BillingAddress
                if ifShipToDifferentAddress is not None:
                    firstNameShip = request.POST.get("first_nameShip")
                    lastNameShip = request.POST.get("last_nameShip")
                    areaShip = (
                        request.POST.get("address_line_1Ship")
                        + ","
                        + request.POST.get("address_line_2Ship")
                    )
                    countryShip = request.POST.get("countryShip")
                    cityShip = request.POST.get("cityShip")
                    stateShip = request.POST.get("stateShip")
                    pincodeShip = request.POST.get("pincodeShip")
                    emailShip = request.POST.get("emailShip")
                    phoneNumberShip = request.POST.get("phone_numberShip")

                    ShippingAddress = (
                        "Name: "
                        + firstNameShip
                        + " "
                        + lastNameShip
                        + ",\n Address: "
                        + areaShip
                        + ", "
                        + cityShip
                        + ", "
                        + stateShip
                        + ", "
                        + countryShip
                        + ",\n Pincode: "
                        + pincodeShip
                        + ",\n Email: "
                        + emailShip
                        + ",\n Ph: "
                        + phoneNumberShip
                    )

                    if ShippingAddress:
                        order.shipping_address = ShippingAddress
                else:
                    order.shipping_address = BillingAddress

                if ifSaveAddress:
                    s_address = UserAddresses(
                        user=request.user,
                        name=firstName + " " + lastName,
                        address=area,
                        state=state,
                        city=city,
                        pincode=pincode,
                        addPhoneNumber=phoneNumber,
                        set_default=True,
                        email=email,
                        country=country,
                        address_type="Home",
                    )
                    s_address.save()

            else:
                try:
                    user_saved_address = UserAddresses.objects.get(
                        user=request.user, set_default=True
                    )
                    BillingAddress_model = (
                        "Name: "
                        + user_saved_address.name
                        + ",\n Address: "
                        + user_saved_address.address
                        + ", "
                        + user_saved_address.city
                        + ", "
                        + user_saved_address.state
                        + ", "
                        + user_saved_address.country
                        + ",\n Pincode: "
                        + user_saved_address.pincode
                        + ",\n Email: "
                        + user_saved_address.email
                        + ",\n Ph: "
                        + user_saved_address.addPhoneNumber
                        or None
                    )
                    order.billing_address = BillingAddress_model
                    order.shipping_address = BillingAddress_model
                except UserAddresses.DoesNotExist:
                    messages.info(request, "Please Fill the delivery address")
                    return redirect("payment-checkout")

            orderNotes = request.POST.get("checkout-mess") or None

            if orderNotes:
                order.orderNote = orderNotes

        response = api.payment_request_create(
            amount=str(amount),
            purpose="test_purchase",
            buyer_name=user.user_full_name(),
            send_sms=settings.SEND_SMS,
            send_email=settings.SEND_EMAIL,
            email=user.email,
            phone=user.mobileno,
            redirect_url=settings.PAYMENT_SUCCESS_REDIRECT_URL,
            allow_repeated_payments=False,
        )

        order.ref_code = response["payment_request"]["id"]
        order.shipping_address = request.COOKIES.get("shipping_address")
        order.billing_address = request.COOKIES.get("shipping_address")

        order.save()
        # payment_redirect_url = response["payment_request"]["longurl"]
        unique_transaction_id = str(uuid.uuid4())
        pay_page_request = PgPayRequest.pay_page_pay_request_builder(
            merchant_transaction_id=unique_transaction_id,
            amount=100,
            merchant_user_id=id_assigned_to_user_by_merchant,
            callback_url=s2s_callback_url,
        )
        pay_page_response = phonepe_client.pay(pay_page_request)
        pay_page_url = pay_page_response.data.instrument_response.redirect_info.url

        if pay_page_url:
            return redirect(pay_page_url)

        else:
            return redirect("cartview")
    else:
        return redirect("login")


@login_required(login_url="login")
def orderPaymentRequestPhonePe(request, amount):
    """Request for Order Payment using Instamojo Payment Gateway

    Args:
        amount (int): request amount to be collected
    """

    if request.user.is_authenticated:

        order = Order.objects.get(user=request.user.id, ordered=False)

        if request.method == "POST":
            firstName = request.POST.get("first_name")
            lastName = request.POST.get("last_name")
            area = (
                request.POST.get("address_line_1")
                + ","
                + request.POST.get("address_line_2")
            )
            country = request.POST.get("country")
            city = request.POST.get("city")
            state = request.POST.get("state")
            pincode = request.POST.get("pincode")
            email = request.POST.get("email")
            phoneNumber = request.POST.get("phone_number")

            ifSaveAddress = request.POST.get("save-address")
            ifShipToDifferentAddress = request.POST.get("ship-box")

            BillingAddress = (
                "Name: "
                + firstName
                + " "
                + lastName
                + ",\n Address: "
                + area
                + ", "
                + city
                + ", "
                + state
                + ", "
                + country
                + ",\n Pincode: "
                + pincode
                + ",\n Email: "
                + email
                + ",\n Ph: "
                + phoneNumber
                or None
            )

            if (
                pincode != None
                or area != None
                or country != None
                or city != None
                or state != None
            ):
                order.billing_address = BillingAddress
                if ifShipToDifferentAddress is not None:
                    firstNameShip = request.POST.get("first_nameShip")
                    lastNameShip = request.POST.get("last_nameShip")
                    areaShip = (
                        request.POST.get("address_line_1Ship")
                        + ","
                        + request.POST.get("address_line_2Ship")
                    )
                    countryShip = request.POST.get("countryShip")
                    cityShip = request.POST.get("cityShip")
                    stateShip = request.POST.get("stateShip")
                    pincodeShip = request.POST.get("pincodeShip")
                    emailShip = request.POST.get("emailShip")
                    phoneNumberShip = request.POST.get("phone_numberShip")

                    ShippingAddress = (
                        "Name: "
                        + firstNameShip
                        + " "
                        + lastNameShip
                        + ",\n Address: "
                        + areaShip
                        + ", "
                        + cityShip
                        + ", "
                        + stateShip
                        + ", "
                        + countryShip
                        + ",\n Pincode: "
                        + pincodeShip
                        + ",\n Email: "
                        + emailShip
                        + ",\n Ph: "
                        + phoneNumberShip
                    )

                    if ShippingAddress:
                        order.shipping_address = ShippingAddress
                else:
                    order.shipping_address = BillingAddress

                if ifSaveAddress:
                    s_address = UserAddresses(
                        user=request.user,
                        name=firstName + " " + lastName,
                        address=area,
                        state=state,
                        city=city,
                        pincode=pincode,
                        addPhoneNumber=phoneNumber,
                        set_default=True,
                        email=email,
                        country=country,
                        address_type="Home",
                    )
                    s_address.save()

            else:
                try:
                    user_saved_address = UserAddresses.objects.get(
                        user=request.user, set_default=True
                    )
                    BillingAddress_model = (
                        "Name: "
                        + user_saved_address.name
                        + ",\n Address: "
                        + user_saved_address.address
                        + ", "
                        + user_saved_address.city
                        + ", "
                        + user_saved_address.state
                        + ", "
                        + user_saved_address.country
                        + ",\n Pincode: "
                        + user_saved_address.pincode
                        + ",\n Email: "
                        + user_saved_address.email
                        + ",\n Ph: "
                        + user_saved_address.addPhoneNumber
                        or None
                    )
                    order.billing_address = BillingAddress_model
                    order.shipping_address = BillingAddress_model
                except UserAddresses.DoesNotExist:
                    messages.info(request, "Please Fill the delivery address")
                    return redirect("payment-checkout")

            orderNotes = request.POST.get("checkout-mess") or None

            if orderNotes:
                order.orderNote = orderNotes

        order.shipping_address = request.COOKIES.get("shipping_address")
        order.billing_address = request.COOKIES.get("shipping_address")


        # payment_redirect_url = response["payment_request"]["longurl"]
        unique_transaction_id = str(uuid.uuid4())
        order.phonepe_merchant_transaction_id = unique_transaction_id
        order.save()
        pay_page_request = PgPayRequest.pay_page_pay_request_builder(
            merchant_transaction_id=unique_transaction_id,
            amount=100,
            merchant_user_id=id_assigned_to_user_by_merchant,
            merchant_order_id=order.sid,
            redirect_mode="POST",
            callback_url="http://127.0.0.1:8000/cart/payment/phonepe/success/callback/",
            # redirect_mode="REDIRECT",
            redirect_url="http://127.0.0.1:8000/cart/payment/phonepe/success/callback/",
        )
        pay_page_response = phonepe_client.pay(pay_page_request)
        pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
        if pay_page_url:
            # Add Payment Details
            phonepe_transaction_record = PhonePePaymentRequestDetail()
            phonepe_transaction_record.user = request.user
            phonepe_transaction_record.order_id = order
            phonepe_transaction_record.amount = amount
            phonepe_transaction_record.success = pay_page_response.success
            phonepe_transaction_record.code = pay_page_response.code
            phonepe_transaction_record.message = pay_page_response.message
            phonepe_transaction_record.merchant_transaction_id = (
                pay_page_response.data.merchant_transaction_id
            )
            phonepe_transaction_record.transaction_id = (
                pay_page_response.data.transaction_id
            )
            phonepe_transaction_record.redirect_url = pay_page_url
            phonepe_transaction_record.save()
            return redirect(pay_page_url)
        else:
            return redirect("cartview")
    else:
        return redirect("login")


@login_required(login_url="login")
def paymentStatusAndOrderStatusUpdate(request):
    if request.method == "POST":
        print(request.data)
    if request.user:
        user = User.objects.get(pk=request.user.id)
        order = Order.objects.get(user=request.user.id, ordered=False)

        if order.ref_code:
            payment_status = api.payment_request_status(order.ref_code)

            if payment_status["payment_request"]["status"] == "Completed":
                order.ordered = True
                order.status = "ordered"
                order.ordered_date = datetime.now()
                payment = Payment()
                payment.instamojo_id = payment_status["payment_request"]["payments"][0][
                    "payment_id"
                ]
                payment.user = request.user
                payment.amount = payment_status["payment_request"]["payments"][0][
                    "amount"
                ]
                payment.save()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.payment = payment
                order.save()

                for item in order_items:
                    # Vendor Order Details
                    vender_order = VendorOrderDetail()
                    vender_order.vendor = item.item.vendor

                    vender_order.order_id = order.sid
                    product_id = Products.objects.get(id=item.item.id)
                    vender_order.order_item = product_id
                    vender_order.order_item_size = item.size
                    vender_order.order_item_qty = item.quantity
                    vender_order.order_amount = item.get_final_price()
                    vender_order.delivery_address = order.shipping_address
                    vender_order.payment_status = "Paid"
                    vender_order.save()

                    # vendor transaction detail
                    (
                        vender_transaction,
                        created,
                    ) = VendorTransactionDetail.objects.get_or_create(
                        vendor=item.item.vendor,
                        order_id=order.sid,
                    )
                    if created:
                        vender_transaction.total_order_amount = item.get_final_price()
                        vender_transaction.order_receiving_date = datetime.now()
                        vender_transaction.save()

                    else:
                        vender_transaction.total_order_amount += item.get_final_price()
                        vender_transaction.save()

                messages.success(request, "Your order was successful!")
                return redirect("ordersummary", pk=order.id)

            elif payment_status["payment_request"]["status"] == "Pending":
                if len(payment_status["payment_request"]["payments"]) > 0:
                    if (
                        payment_status["payment_request"]["payments"][0]["status"]
                        == "Failed"
                    ):
                        pending_payment = PendingPayment()
                        pending_payment.order_id = payment_status["payment_request"][
                            "id"
                        ]
                        pending_payment.order_payment_id = payment_status[
                            "payment_request"
                        ]["payments"][0]["payment_id"]
                        pending_payment.phone = payment_status["payment_request"][
                            "phone"
                        ]
                        pending_payment.email = payment_status["payment_request"][
                            "email"
                        ]
                        pending_payment.buyer_name = payment_status["payment_request"][
                            "buyer_name"
                        ]
                        pending_payment.amount = payment_status["payment_request"][
                            "amount"
                        ]
                        pending_payment.purpose = payment_status["payment_request"][
                            "purpose"
                        ]
                        pending_payment.status = payment_status["payment_request"][
                            "status"
                        ]
                        pending_payment.created_at = payment_status["payment_request"][
                            "created_at"
                        ]
                        pending_payment.modified_at = payment_status["payment_request"][
                            "modified_at"
                        ]
                        pending_payment.api_response = payment_status
                        pending_payment.save()
                        return redirect("failed-payment", pk=order.id)

                else:
                    pending_payment = PendingPayment()
                    pending_payment.order_id = payment_status["payment_request"]["id"]
                    pending_payment.phone = payment_status["payment_request"]["phone"]
                    pending_payment.email = payment_status["payment_request"]["email"]
                    pending_payment.buyer_name = payment_status["payment_request"][
                        "buyer_name"
                    ]
                    pending_payment.amount = payment_status["payment_request"]["amount"]
                    pending_payment.purpose = payment_status["payment_request"][
                        "purpose"
                    ]
                    pending_payment.status = payment_status["payment_request"]["status"]
                    pending_payment.api_response = payment_status
                    pending_payment.created_at = payment_status["payment_request"][
                        "created_at"
                    ]
                    pending_payment.modified_at = payment_status["payment_request"][
                        "modified_at"
                    ]
                    pending_payment.save()
                    return redirect("pending-payment", pk=order.id)


@login_required(login_url="login")
def paymentStatusAndOrderStatusUpdatePhonePe(request):
    return render(request, "checkout/thankyou.html")


@login_required(login_url="login")
def checkoutPage(request):
    order = Order.objects.get(user=request.user, ordered=False)
    try:
        address = UserAddresses.objects.filter(user=request.user)
        primary_address = UserAddresses.objects.get(user=request.user, set_default=True)
    except UserAddresses.DoesNotExist:
        address = []
        primary_address = ""

    totalAmount = round(order.get_total(), 2)
    ShippingCharges = 40
    if totalAmount > 600:
        ShippingCharges = 0
    totalAmount += ShippingCharges

    # razorpay api call data collect
    request_data = {
        "amount": int(order.total_amount_at_checkout() * 100),
        "currency": "INR",
        "receipt": order.sid,
    }
    razorpay_response = razorpay_api.order.create(data=request_data)
    order.razorpay_order_id = razorpay_response["id"]
    order.save()

    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "orderItems": order,
        "totalAmount": ceil(order.total_amount_at_checkout()),
        "shippingCharges": ceil(ShippingCharges),
        "address": address,
        "gst_amount": ceil(order.gst_amount()),
        "primary_address": primary_address,
        "razorpay_order_id": razorpay_response["id"],
        "razorpay_key_id": settings.RAZORPAY_API_KEY,
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "checkout/checkout.html", context)


class CartAddView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )

    def get(self, request, format=None):
        try:
            itemsForCartPage = Order.objects.get(user=request.user.id, ordered=False)
            serializer = OrderSerializer(instance=itemsForCartPage)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"data": "No items in cart"}, status=status.HTTP_204_NO_CONTENT
            )

    def post(self, request, format=None):
        data = request.POST
        product_pk = data.get("product")
        quantity = int(data.get("quantity"))
        req_size = data.get("size")

        item = get_object_or_404(
            Products,
            pk=product_pk,
            available_sizes__in=ProductSize.objects.filter(code=req_size),
        )
        order_item, created = Cart.objects.get_or_create(
            item=item, size=req_size, user=request.user, ordered=False
        )
        if created:
            if quantity == None:
                quantity = 0

            order_item.quantity = quantity
            order_item.save()

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if (
                order.items.filter(item__id=item.id, size=req_size).exists()
                and item.stock > 0
            ):
                order_item.quantity += quantity
                item.stock = item.stock - quantity
                item.save()
                order_item.save()
            elif item.stock > 0:
                order.items.add(order_item)
                item.stock = item.stock - quantity
                item.save()
            else:
                return Response(
                    {"data": "Item out of Stock"}, status=status.HTTP_200_OK
                )
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)

            order.items.add(order_item)
        serializer = OrderSerializer(instance=order_qs, many=True)
        return Response(
            {
                "cart": serializer.data,
                "amount": ceil(order.get_total()),
                "tmax_amount": ceil(order.get_max_total()),
                "qty": order.get_quantity(),
                "item_qty": order_item.quantity,
                "item_tprice": ceil(order_item.get_total_item_price()),
                "item_dprice": ceil(order_item.get_amount_saved()),
                "amount_at_checkout": ceil(order.total_amount_at_checkout()),
                "shipping": ceil(order.shipping_charge()),
                "gst_amount": ceil(order.gst_amount()),
            },
            status=status.HTTP_200_OK,
        )


class CartRemoveView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )

    def post(self, request, format=None):
        data = request.data
        product_pk = data.get("product")
        quantity = int(data.get("quantity"))
        req_size = data.get("size")

        item = get_object_or_404(
            Products,
            pk=product_pk,
            available_sizes__in=ProductSize.objects.filter(code=req_size),
        )

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__id=item.id, size=req_size).exists():
                order_item = Cart.objects.filter(
                    item=item, size=req_size, user=request.user, ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    item.stock += 1
                    item.save()

                    return Response(
                        {
                            "cart": "Item updated",
                            "amount": ceil(order.get_total()),
                            "tmax_amount": ceil(order.get_max_total()),
                            "qty": order.get_quantity(),
                            "item_qty": order_item.quantity,
                            "item_tprice": ceil(order_item.get_total_item_price()),
                            "item_dprice": ceil(order_item.get_amount_saved()),
                            "amount_at_checkout": ceil(
                                order.total_amount_at_checkout()
                            ),
                            "shipping": ceil(order.shipping_charge()),
                            "gst_amount": ceil(order.gst_amount()),
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    order.items.remove(order_item)
                    order_item.delete()
                    item.stock += 1
                    item.save()
                    return Response(
                        {
                            "cart": "Item updated",
                            "amount": ceil(order.get_total()),
                            "tmax_amount": ceil(order.get_max_total()),
                            "qty": order.get_quantity(),
                            "item_qty": 0,
                            "item_tprice": 0,
                            "item_dprice": 0,
                            "amount_at_checkout": ceil(
                                order.total_amount_at_checkout()
                            ),
                            "shipping": ceil(order.shipping_charge()),
                            "gst_amount": ceil(order.gst_amount()),
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {
                        "cart": "Item not available in cart",
                        "amount": ceil(order.get_total()),
                        "tmax_amount": ceil(order.get_max_total()),
                        "qty": ceil(order.get_quantity()),
                        "item_qty": 0,
                        "item_tprice": 0,
                        "item_dprice": 0,
                        "amount_at_checkout": ceil(order.total_amount_at_checkout()),
                        "shipping": ceil(order.shipping_charge()),
                        "gst_amount": ceil(order.gst_amount()),
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response({"cart": "No Active Orders"}, status=status.HTTP_201_OK)


@login_required(login_url="login")
def order_summary(request, pk):
    if request.user:
        order = Order.objects.get(user=request.user.id, pk=pk)
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "order": order,
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "checkout/thankyou.html", context)


def pending_payment_page(request, pk):
    if request.user:
        order = Order.objects.get(user=request.user.id, pk=pk)
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "order": order,
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "checkout/payment-failed.html", context)


def failed_payment_page(request, pk):
    if request.user:
        order = Order.objects.get(user=request.user.id, pk=pk)
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    context = {
        "order": order,
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "checkout/payment-failed.html", context)


@login_required(login_url="login")
def addToCartWithSizeQuantity(request, pk):
    current_site = get_current_site(request)
    domain_name = request.get_host()

    previous_page = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        size = request.POST.get("choose-size")
        qty = request.POST.get("pro-qty")

        if size == None:
            messages.info(request, "Please select the item size")
            return redirect(previous_page)

    user = Token.objects.get(user=request.user)
    api_url = "http://" + domain_name + "/cart/customer/order/add/"
    headers = {"Authorization": f"Token {user}"}
    data = {"product": pk, "quantity": qty, "size": size}
    # print(data)
    response = requests.post(url=api_url, data=data, headers=headers)
    # print(response.json())

    messages.info(request, "Item Added to Cart Successfully!")
    return redirect(previous_page)


@login_required(login_url="login")
def razorpay_success_redirect(request):
    razorpay_order_id = request.GET.get("razorpay_order_id")
    razorpay_payment_id = request.GET.get("razorpay_payment_id")
    if request.user:
        order = Order.objects.get(user=request.user.id, ordered=False)
        # order = Order.objects.get(razorpay_order_id=razorpay_order_id, ordered=False)

        order.ordered = True
        order.status = "ordered"
        order.ordered_date = datetime.now()
        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.razorpay_payment_id = razorpay_payment_id
        order.save()

    messages.success(request, "Your order was successful!")
    return redirect("ordersummary", pk=order.id)
