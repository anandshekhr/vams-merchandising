from datetime import date, datetime, timedelta
import http.cookies
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth, messages
from .serializers import UpdateUserSerializer
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from products.serializer import userSerializer
from cart.models import Order
from rest_framework.decorators import api_view, permission_classes
from .models import *
from datetime import datetime, timezone
from django.http import JsonResponse
from django.utils.timezone import utc
from .utils import OTPManager
from random import randint
from cart.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
import requests

User = get_user_model()


# Create your views here.

def register(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        sign_up = request.POST.get('sing-up')

        if password == confirm_password:
            if User.objects.filter(mobileno=phone_number).exists():
                messages.info(request, "mobile number already exist")
                return redirect('register')
            elif sign_up is None:
                messages.info(request, "Please accept Terms & Conditions")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email already exists")
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        first_name=first_name, last_name=last_name, mobile=phone_number, email=email, username=username, password=password)
                    user.save()
                    token, created = Token.objects.get_or_create(user=user)
                    messages.success(
                        request, f"Account Registered, Please Login Again!")
                    return redirect('login')
        else:
            messages.info(request, "Password didn;t matched!")
            return redirect('register')
    else:
        return render(request, 'register.html')


def set_token_cookie(response, token):

    cookie = http.cookies.SimpleCookie()
    cookie['token'] = token
    cookie['token']['expires'] = 60*60*24*30
    response.set_cookie(key='token', value=token, expires=3600*24*30)


def login(request):
    token = ""
    if request.method == 'POST':
        mobileno = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = auth.authenticate(mobileno=mobileno, password=password)

        if user is not None:
            auth.login(request, user)
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                messages.info(request, 'Token not generated')
            response = redirect('home')
            set_token_cookie(response, token)
            return response
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password_reset_request = requests.post(
            'http://127.0.0.1:8000/api/v1/account/password/reset/', {'email': email})
        # print(password_reset_request.text)
        if password_reset_request.status_code == 200:
            print("200 aaya,, redirecting !!!")
            return redirect('password-reset-web-page')
        else:
            print(password_reset_request.text)
    return render(request, 'forgot-password.html')


def password_reset_method(request):
    print("yaha aaya")
    # if request.method == 'POST':
    #     password = request.POST.get('password')

    return render(request, 'reset-password.html')


class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = userSerializer

    def get(self, request, format=None):
        user = User.objects.get(pk=self.request.user.id)
        serializer = userSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def profileUser(request):
    if request.user:
        userdetails = User.objects.get(pk=request.user.id)
        context = {
            'user': userdetails
        }
    return render(request, "profile.html", context)


def userOrderDetail(request):
    if request.user:
        orders = Order.objects.filter(user=request.user.id, ordered=True)
        context = {
            'orders': orders
        }
    return render(request, "user-order-detail.html", context)


def userOrderDetailExpanded(request, pk):
    if request.user:
        order_detail = Order.objects.get(user=request.user.id, pk=pk)
        expected_delivery = datetime.strptime(
            str(order_detail.ordered_date), '%Y-%m-%d %H:%M:%S.%f%z')+timedelta(days=6)
    context = {
        'orders': order_detail,
        'expected_delivery_date': expected_delivery
    }
    return render(request, "user/order-detail.html", context)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def get_otp(request):
    try:
        # device = Device.objects.get(auth_token=request.data.get('auth_token'))
        country_code = request.data.get('country_code')
        phone_number = request.data.get('phone_number')
        fake_otp = bool(request.data.get('fake_otp'))

        try:
            last_sms = DeviceOtp.objects.filter(
                number=phone_number).latest('created_date')
            if last_sms:
                timediff = datetime.now(timezone.utc) - last_sms.created_date
                if timediff.total_seconds() < 15:
                    return JsonResponse({'Status': "Sent"})
        except Exception as e:
            print(e)
            pass

        if OTPManager.send_otp(fake_otp,
                               int(request.data.get('otp')) if fake_otp else randint(
                                   100000, 999999),
                               country_code,
                               phone_number,
                               ):
            return Response({'Status': "Sent"}, status=status.HTTP_200_OK)
        return JsonResponse({'Error': "You have exceeded your attempts."})
    except Exception as e:
        print(e)
        return Response({'Error': "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def verify_otp(request):
    try:
        # Device.objects.get(auth_token=request.data.get('auth_token'))
        phone_number = request.data.get('phone_number')
        country_code = request.data.get('country_code')
        web = bool(request.data.get('web'))
        otp = request.data.get('otp')
        print('otp is - ', otp)
        if not web:
            return OTPManager.verify_otp(otp, country_code, phone_number, web)
        else:
            user_r = OTPManager.verify_otp(
                otp, country_code, phone_number, web)
            auth.login(request, user_r)
            return Response({"status": "OK"}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({'Error': "Invalid Data"}, status=status.HTTP_200_OK)


def profileDashboard(request):
    try:
        orders = Order.objects.filter(
            user=request.user.id)
        
        p = Paginator(orders, 2)  # creating a paginator object
        # getting the desired page number from url
        page_number = request.GET.get('page')
        try:
            # returns the desired page object
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        except Exception as e:
            return HttpResponse(e)

        pending_orders = Order.objects.filter(
            user=request.user.id, ordered=False)
        completed_orders_count = Order.objects.filter(
            user=request.user.id, ordered=True).count()

        context = {
            'orders': orders,
            'page_orders': page_obj,
            'completed_orders': completed_orders_count,
            'pending_orders': pending_orders.count()
        }
        return render(request, "user/dashboard.html", context)
    except Exception as e:
        print(e)
        context = {
            'page_orders': [0]
        }
        return render(request, "user/dashboard.html", context)


def user_address(request):
    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        area = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        address_type = request.POST.get('address-type')
        if request.POST.get('flexCheckStock') is not None:
            set_default = request.POST.get('flexCheckStock')
        else:
            set_default = False
        s_address = UserAddresses(user=request.user, name=first_name+" "+last_name, address=area, state=state, city=city,
                                  pincode=pincode, addPhoneNumber=phone, set_default=set_default, email=email, country=country, address_type=address_type)
        s_address.save()
    address = UserAddresses.objects.filter(user=request.user.id)
    context = {'address': address}
    return render(request, "user/address.html", context)


@login_required(login_url="login")
def user_orders(request):
    if request.user:
        # fetching all post objects from database
        orders = Order.objects.filter(user=request.user.id)
        print(len(orders))

        # if len(orders) > 2:
        p = Paginator(orders, 2)  # creating a paginator object
        # getting the desired page number from url
        page_number = request.GET.get('page')
        try:
            # returns the desired page object
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        except Exception as e:
            return HttpResponse(e)
        context = {'page_orders': page_obj}

        # else:
        #     context = {'page_orders': orders}

    return render(request, "user/orders.html", context)


def user_payment(request):
    if request.method == "POST":
        card_number = request.POST.get('card-number')
        card_holder_name = request.POST.get('card-holder')
        exp_month = request.POST.get('exp-month')
        exp_year = request.POST.get('exp-year')
        if request.POST.get('flexCheckStock') is not None:
            default = request.POST.get('flexCheckStock')
        else:
            default = False

        save_model = Cards(user=request.user, card_number=card_number, card_holder_name=card_holder_name,
                           exp_month=exp_month, exp_year=exp_year, set_as_default=default)
        save_model.save()
    saved_cards = Cards.objects.filter(user=request.user)
    return render(request, "user/payment.html", {'cards': saved_cards})


def user_coupon(request):
    return render(request, "user/coupon.html")


def user_notification(request):
    notifications = request.user.notifications.filter(is_read=False)
    return render(request, "user/notification.html", {'notifications': notifications})


def delete_user_address(request, pk):
    address = get_object_or_404(UserAddresses, user=request.user.id, pk=pk)
    address.delete()
    return redirect("profile-address")


def set_primary_address(request, pk):
    print("calling set function")
    address = UserAddresses.objects.get(user=request.user.id, pk=pk)
    if address.set_default == False:
        address.set_default == True
        address.save()
    return redirect('profile-address')


def userDashboard(request):
    return render(request, "user/dashboard.html")


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
