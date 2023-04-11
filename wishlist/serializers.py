from rest_framework import serializers
from .models import *
from products.serializer import *
from django.contrib.auth import authenticate, get_user_model

user = get_user_model()


class WishlistItemSerializer(serializers.ModelSerializer):
    item = ProductsSerializer()

    class Meta:
        model = WishlistItems
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = '__all__'
