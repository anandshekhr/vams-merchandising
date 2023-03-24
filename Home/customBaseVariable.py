from cart.models import *
from .models import *
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.shortcuts import get_object_or_404


def addVariableBaseTemplate(request):
    try:
        cartitems = Order.objects.get(user=request.user.id, ordered=False)
        saved_cards = Cards.objects.filter(user = request.user.id)
        saved_address = UserAddresses.objects.filter(user=request.user.id)
        return {
            'cart': cartitems,
            'saved_cards':saved_cards,
            'saved_address':saved_address
            }
    except Order.DoesNotExist:
        return {
            'cart': {
                'name':'Does not exist'
            }
        }

    
