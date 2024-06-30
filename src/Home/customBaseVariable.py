from cart.models import *
from wishlist.models import *
from .models import *
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache



def addVariableBaseTemplate(request):
    try:
        cartitems = Order.objects.get(user=request.user.id, ordered=False)
    
    except Order.DoesNotExist:
        cartitems = "Does not exist"
    
    
    try:
        wishlist_items = Wishlist.objects.get(user=request.user.id)
    
    except Wishlist.DoesNotExist:
        wishlist_items = "Does not exist"

    return {
        'cart': cartitems,
        'wishlist': wishlist_items,
    }

    
