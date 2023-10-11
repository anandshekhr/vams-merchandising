from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, get_user_model

user = get_user_model()

class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = '__all__'

class SellerStoreDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerStoreDetails
        fields = '__all__'