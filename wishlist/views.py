# from django.shortcuts import render
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
from user.models import UserAddresses
from instamojo_wrapper import Instamojo
from django.contrib.sites.shortcuts import get_current_site
from Home.views import get_meta_data

api = Instamojo(
    api_key=settings.API_KEY,
    auth_token=settings.AUTH_TOKEN,
    endpoint="https://test.instamojo.com/api/1.1/",
)

User = get_user_model()
# Create your views here.


@login_required(login_url="login")
def wishlistView(request):
    title, desc, key, canonical = get_meta_data(request.path, request.get_host())

    items = Wishlist.objects.get(user=request.user)
    context = {
        "items": items,
        "page_title": title,
        "description": desc,
        "keyword": key,
        "canonical": canonical,
    }
    return render(request, "wishlist/wishlist.html", context)


def deleteItemFromWishlist(request, pk):
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
    item = WishlistItems.objects.filter(item=pk)[0]
    item.delete()

    # delete from Wishlist models
    wishlist_item = Wishlist.objects.filter(user=request.user)[0]
    wishlist_item.items.remove(item)
    return redirect(previous_page)


@login_required(login_url="login")
def addToWishlist(request, pk):
    # to return to previous page
    previous_page = request.META.get("HTTP_REFERER")

    item = get_object_or_404(Products, id=pk)
    order_item, created = WishlistItems.objects.get_or_create(
        item=item, user=request.user
    )

    order_qs = Wishlist.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item was added to your Wishlist!")
            return redirect(previous_page)

        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your Wishlist!")
            return redirect(previous_page)

    else:
        order = Wishlist.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your Wishlist!")
        return redirect(previous_page)


class AddToWishlistAPI(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )

    def get(self, request, format=None):
        try:
            itemsForCartPage = Wishlist.objects.get(user=request.user)
            serializer = WishlistSerializer(instance=itemsForCartPage)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            return Response(
                {"data": "No items in cart"}, status=status.HTTP_204_NO_CONTENT
            )

    def post(self, request, format=None):
        data = request.data
        product_pk = data.get("product")
        item = get_object_or_404(Products, id=product_pk)
        order_item, created = WishlistItems.objects.get_or_create(
            item=item,
            user=request.user,
        )
        order_qs = Wishlist.objects.filter(user=request.user)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__id=item.id).exists():
                order_item.quantity += 1
                order_item.save()
            else:
                order.items.add(order_item)
        else:
            order = Wishlist.objects.create(user=request.user)
            order.items.add(order_item)
        serializer = WishlistSerializer(instance=order_qs, many=True)
        return Response(
            {
                "wishlist": serializer.data,
                "amount": order.get_total(),
                "tmax_amount": order.get_max_total(),
                "qty": order.get_quantity(),
                "item_qty": order_item.quantity,
                "item_tprice": order_item.get_total_item_price(),
                "item_dprice": order_item.get_amount_saved(),
            },
            status=status.HTTP_200_OK,
        )
