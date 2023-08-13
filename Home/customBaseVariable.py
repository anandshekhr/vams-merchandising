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
        wishlist_items = Wishlist.objects.get(user=request.user.id)
        return {
            'cart': cartitems,
            'wishlist':wishlist_items,
            }
    except Order.DoesNotExist:
        return {
            'cart': {
                'name':'Does not exist'
            },
            'wishlist':{
                'name':'Does not exist'
            }
        }

    except Wishlist.DoesNotExist:
        return {
            'cart': {
                'name': 'Does not exist'
            },
            'wishlist': {
                'name': 'Does not exist'
            }
        }

    
