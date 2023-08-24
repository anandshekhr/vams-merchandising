# from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, HttpResponse, get_list_or_404, get_object_or_404
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
from user.models import UserAddresses
from instamojo_wrapper import Instamojo
import requests
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

User = get_user_model()


@login_required(login_url="login")
def cartCheckoutPageView(request):
    counter = 0
    a = 0
    b = 0
    try:
        if request.user:
            itemsForCartPage = Order.objects.get(
                user=request.user.id, ordered=False)

        a = round(itemsForCartPage.get_total(), 2)
        counter = len(itemsForCartPage.items.all())

        if a > 599:
            delivery_charges = 0
        else:
            delivery_charges = 40

        grandtotal = a + delivery_charges

        context = {
            'object': itemsForCartPage,
            'delivery': delivery_charges,
            'totalquantity': counter,
            'grandtotal': grandtotal
        }
    except Order.DoesNotExist:
        context = {
            'object': 0,
            'delivery': 0,
            'totalquantity': 0,
            'grandtotal': 0
        }
    return render(request, "cart.html", context)


@login_required(login_url="login")
def addToCart(request, pk, size):

    item = get_object_or_404(Products, id=pk)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        size=size,
        user=request.user,
        ordered=False
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
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cartview")


@login_required(login_url="login")
def moveToCart(request, pk):
    # delete from wishlistItems models
    # iitem = WishlistItems.objects.filter(item=pk)
    # for ir in iitem:
    #     ir.item.delete()

    # delete from Wishlist models
    # wishlist_item = Wishlist.objects.filter(user=request.user)[0]
    # wishlist_item.items.remove(iitem)

    item = get_object_or_404(Products, id=pk)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
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
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cartview")


def deleteItemFromCart(request, pk):
    """Delete Items from Wishlist

    Args:
        request (_type_): _description_
        pk (int): product ID

    Returns:
        _type_: _description_
    """

    # delete from wishlistItems models
    item = Cart.objects.filter(item=pk, user=request.user, ordered=False)[0]
    item.delete()

    # delete from Wishlist models
    wishlist_item = Order.objects.filter(user=request.user, ordered=False)[0]
    wishlist_item.items.remove(item)

    return redirect('cartview')


@login_required(login_url="login")
def removeSingleItemFromCart(request, pk):
    if request.user:
        user_details = UserAddresses.objects.get(user=request.user.id)
    item = get_object_or_404(StoreProductsDetails, products=pk,
                             store__storeServicablePinCodes__contains=[user_details.pincode])
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__products__id=item.products.id).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
                ordered=False
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
def orderPaymentRequest(request, amount):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        order = Order.objects.get(user=request.user.id, ordered=False)

        if request.method == "POST":
            firstName = request.POST.get('first_name')
            lastName = request.POST.get('last_name')
            area = request.POST.get('address_line_1') + \
                ","+request.POST.get('address_line_2')
            country = request.POST.get('country')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            email = request.POST.get('email')
            phoneNumber = request.POST.get('phone_number')

            ifSaveAddress = request.POST.get('save-address')
            ifShipToDifferentAddress = request.POST.get('ship-box')

            BillingAddress = "Name: "+firstName+" "+lastName+",\n Address: "+area+", "+city+", "+state + \
                ", "+country+",\n Pincode: "+pincode+",\n Email: " + \
                email+",\n Ph: "+phoneNumber or None

            if pincode != None or area != None or country != None or city != None or state != None:
                order.billing_address = BillingAddress
                if ifShipToDifferentAddress is not None:
                    firstNameShip = request.POST.get('first_nameShip')
                    lastNameShip = request.POST.get('last_nameShip')
                    areaShip = request.POST.get('address_line_1Ship')+"," + \
                        request.POST.get('address_line_2Ship')
                    countryShip = request.POST.get('countryShip')
                    cityShip = request.POST.get('cityShip')
                    stateShip = request.POST.get('stateShip')
                    pincodeShip = request.POST.get('pincodeShip')
                    emailShip = request.POST.get('emailShip')
                    phoneNumberShip = request.POST.get('phone_numberShip')

                    ShippingAddress = "Name: "+firstNameShip+" "+lastNameShip+",\n Address: "+areaShip+", "+cityShip+", " + \
                        stateShip+", "+countryShip+",\n Pincode: "+pincodeShip + \
                        ",\n Email: "+emailShip+",\n Ph: "+phoneNumberShip

                    if ShippingAddress:
                        order.shipping_address = ShippingAddress
                else:
                    order.shipping_address = BillingAddress

                if ifSaveAddress:
                    s_address = UserAddresses(user=request.user, name=firstName+" "+lastName, address=area, state=state, city=city,
                                              pincode=pincode, addPhoneNumber=phoneNumber, set_default=True, email=email, country=country, address_type="Home")
                    s_address.save()

            else:
                try:
                    user_saved_address = UserAddresses.objects.get(
                        user=request.user, set_default=True)
                    BillingAddress_model = "Name: "+user_saved_address.name+",\n Address: "+user_saved_address.address+", "+user_saved_address.city+", "+user_saved_address.state + \
                        ", "+user_saved_address.country+",\n Pincode: "+user_saved_address.pincode+",\n Email: " + \
                        user_saved_address.email+",\n Ph: "+user_saved_address.addPhoneNumber or None
                    order.billing_address = BillingAddress_model
                    order.shipping_address = BillingAddress_model
                except UserAddresses.DoesNotExist:
                    messages.info(request, "Please Fill the delivery address")
                    return redirect('payment-checkout')

            orderNotes = request.POST.get('checkout-mess') or None

            if orderNotes:
                order.orderNote = orderNotes
        domain_name = request.get_host()
        response = api.payment_request_create(
            amount=str(amount),
            purpose='test_purchase',
            buyer_name=user.user_full_name(),
            send_sms=settings.SEND_SMS,
            send_email=settings.SEND_EMAIL,
            email=user.email,
            phone=user.mobileno,
            redirect_url=settings.PAYMENT_SUCCESS_REDIRECT_URL,
            allow_repeated_payments=False
        )
        # print(response)
        order.ref_code = response['payment_request']['id']
        order.save()
        payment_redirect_url = response['payment_request']['longurl']
        if payment_redirect_url:
            context = {
                'payment_url': payment_redirect_url
            }
            return render(request, "paymentredirect.html", context)
        else:
            return redirect("cartview")
    else:
        return redirect("login")


@login_required(login_url="login")
def paymentStatusAndOrderStatusUpdate(request):
    if request.user:
        user = User.objects.get(pk=request.user.id)
        order = Order.objects.get(user=request.user.id, ordered=False)

        if order.ref_code:
            payment_status = api.payment_request_status(order.ref_code)

            if payment_status['payment_request']['status'] == 'Completed':
                order.ordered = True
                order.status = 'ordered'
                order.ordered_date = datetime.now()
                payment = Payment()
                payment.instamojo_id = payment_status['payment_request']['payments'][0]['payment_id']
                payment.user = request.user
                payment.amount = payment_status['payment_request']['payments'][0]['amount']
                payment.save()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.payment = payment
                order.save()
                messages.success(request, "Your order was successful!")
                return redirect("ordersummary", pk=order.id)

            elif payment_status['payment_request']['status'] == 'Pending':

                if len(payment_status['payment_request']['payments']) > 0:

                    if payment_status['payment_request']['payments'][0]['status'] == 'Failed':
                        pending_payment = PendingPayment()
                        pending_payment.order_id = payment_status['payment_request']['id']
                        pending_payment.order_payment_id = payment_status[
                            'payment_request']['payments'][0]['payment_id']
                        pending_payment.phone = payment_status['payment_request']['phone']
                        pending_payment.email = payment_status['payment_request']['email']
                        pending_payment.buyer_name = payment_status['payment_request']['buyer_name']
                        pending_payment.amount = payment_status['payment_request']['amount']
                        pending_payment.purpose = payment_status['payment_request']['purpose']
                        pending_payment.status = payment_status['payment_request']['status']
                        pending_payment.created_at = payment_status['payment_request']['created_at']
                        pending_payment.modified_at = payment_status['payment_request']['modified_at']
                        pending_payment.api_response = payment_status
                        pending_payment.save()
                        return redirect("failed-payment", pk=order.id)

                else:
                    pending_payment = PendingPayment()
                    pending_payment.order_id = payment_status['payment_request']['id']
                    pending_payment.phone = payment_status['payment_request']['phone']
                    pending_payment.email = payment_status['payment_request']['email']
                    pending_payment.buyer_name = payment_status['payment_request']['buyer_name']
                    pending_payment.amount = payment_status['payment_request']['amount']
                    pending_payment.purpose = payment_status['payment_request']['purpose']
                    pending_payment.status = payment_status['payment_request']['status']
                    pending_payment.api_response = payment_status
                    pending_payment.created_at = payment_status['payment_request']['created_at']
                    pending_payment.modified_at = payment_status['payment_request']['modified_at']
                    pending_payment.save()
                    return redirect("pending-payment", pk=order.id)


@login_required(login_url="login")
def checkoutPage(request):
    Items = Order.objects.get(user=request.user, ordered=False)
    totalAmount = round(Items.get_total(), 2)
    ShippingCharges = 40
    if totalAmount > 599:
        ShippingCharges = 0
    totalAmount += ShippingCharges
    context = {'orderItems': Items, 'totalAmount': totalAmount,
               'shippingCharges': ShippingCharges}
    return render(request, "checkout.html", context)


class CartAddView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.BasicAuthentication,
                              authentication.SessionAuthentication, authentication.TokenAuthentication)

    def get(self, request, format=None):
        try:
            itemsForCartPage = Order.objects.get(
                user=request.user.id, ordered=False)
            serializer = OrderSerializer(instance=itemsForCartPage)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'data': 'No items in cart'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        data = request.POST
        print(data)
        product_pk = data.get('product')
        quantity = int(data.get('quantity'))
        req_size = data.get('size')
        item = get_object_or_404(
            Products, pk=product_pk, available_sizes__contains=[req_size])
        order_item, created = Cart.objects.get_or_create(
            item=item,
            size=req_size,
            quantity=quantity,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__id=item.id, size=req_size).exists() and item.stock > 0:
                order_item.quantity += quantity
                item.stock = item.stock - quantity
                item.save()
                order_item.save()
            elif item.stock > 0:
                order.items.add(order_item)
                item.stock = item.stock - quantity
                item.save()
            else:
                return Response({'data': 'Item out of Stock'}, status=status.HTTP_200_OK)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)

            order.items.add(order_item)
        serializer = OrderSerializer(instance=order_qs, many=True)
        return Response({'cart': serializer.data, 'amount': order.get_total(), 'tmax_amount': order.get_max_total(), 'qty': order.get_quantity(), 'item_qty': order_item.quantity, "item_tprice": order_item.get_total_item_price(), "item_dprice": order_item.get_amount_saved()}, status=status.HTTP_200_OK)


class CartRemoveView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.BasicAuthentication,
                              authentication.SessionAuthentication, authentication.TokenAuthentication)

    def post(self, request, format=None):
        data = request.data
        product_pk = data.get('product')
        quantity = int(data.get('quantity'))
        req_size = data.get('size')

        item = get_object_or_404(
            Products, pk=product_pk, available_sizes__contains=[req_size])

        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__id=item.id, size=req_size).exists():
                order_item = Cart.objects.filter(
                    item=item,
                    size=req_size,
                    user=request.user,
                    ordered=False
                )[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    item.stock += 1
                    item.save()

                    return Response({'cart': 'Item updated', 'amount': order.get_total(), 'tmax_amount': order.get_max_total(), 'qty': order.get_quantity(), 'item_qty': order_item.quantity, "item_tprice": order_item.get_total_item_price(), "item_dprice": order_item.get_amount_saved()}, status=status.HTTP_200_OK)
                else:
                    order.items.remove(order_item)
                    order_item.delete()
                    item.stock += 1
                    item.save()
                    return Response({'cart': 'Item updated', 'amount': order.get_total(), 'tmax_amount': order.get_max_total(), 'qty': order.get_quantity(), 'item_qty': 0, "item_tprice": 0, "item_dprice": 0}, status=status.HTTP_200_OK)
            else:
                return Response({'cart': 'Item not available in cart', 'amount': order.get_total(), 'tmax_amount': order.get_max_total(), 'qty': order.get_quantity(), 'item_qty': 0, "item_tprice": 0, "item_dprice": 0}, status=status.HTTP_200_OK)
        else:
            return Response({'cart': 'No Active Orders'}, status=status.HTTP_201_OK)


@login_required(login_url="login")
def order_summary(request, pk):
    if request.user:
        order = Order.objects.get(user=request.user.id, pk=pk)

    context = {
        'order': order
    }
    return render(request, "thankyou.html", context)


def pending_payment_page(request, pk):
    if request.user:
        order = Order.objects.get(user=request.user.id, pk=pk)

    context = {
        'order': order
    }
    return render(request, "payment-failed.html", context)


def failed_payment_page(request, pk):
    if request.user:
        order = Order.objects.get(user=request.user.id, pk=pk)

    context = {
        'order': order
    }
    return render(request, "payment-failed.html", context)


@login_required(login_url="login")
def addToCartWithSizeQuantity(request, pk):

    current_site = get_current_site(request)
    domain_name = request.get_host()

    previous_page = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        size = request.POST.get('choose-size')
        qty = request.POST.get('pro-qty')

        if size == None:
            messages.info(request, "Please select the item size")
            return redirect(previous_page)

    user = Token.objects.get(user=request.user)
    api_url = "http://"+domain_name+"/api/v1/customer/order/add/"
    headers = {'Authorization': f'Token {user}'}
    data = {'product': pk, 'quantity': qty, 'size': size}
    # print(data)
    response = requests.post(url=api_url, data=data, headers=headers)
    # print(response.json())

    messages.info(request, "Item Added to Cart Successfully!")
    return redirect(previous_page)
