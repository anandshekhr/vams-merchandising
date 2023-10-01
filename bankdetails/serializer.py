from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, get_user_model

user = get_user_model()

class ifscCodeDetailsSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = ifscCodeDetails
        fields='__all__'