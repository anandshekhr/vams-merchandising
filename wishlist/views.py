# from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth, messages
from rest_framework import generics, status, authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Products
from .models import *
# from .serializers import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from stores.models import *
from user.models import UserAddresses
from instamojo_wrapper import Instamojo
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

User = get_user_model()
# Create your views here.

def wishlistView(request):
    items = Wishlist.objects.get(user=request.user)
    context = {'items':items}
    return render(request,"wishlist.html",context)

def deleteItemFromWishlist(request,pk):
    """Delete Items from Wishlist

    Args:
        request (_type_): _description_
        pk (int): product ID

    Returns:
        _type_: _description_
    """
    
    #delete from wishlistItems models
    item = WishlistItems.objects.filter(item = pk)[0]
    item.delete()

    # delete from Wishlist models
    wishlist_item = Wishlist.objects.filter(user =request.user)[0]
    wishlist_item.items.remove(item)
    
    return redirect('wishlist-view')

@login_required
def addToWishlist(request, pk):

    item = get_object_or_404(Products, id=pk)
    order_item, created = WishlistItems.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_qs = Wishlist.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("wishlist-view")

        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("wishlist-view")

    else:
        order = Wishlist.objects.create(
            user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("wishlist-view")
