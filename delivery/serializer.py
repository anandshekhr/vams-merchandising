from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, get_user_model

user = get_user_model()

class PincodeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PincodeDetail
        fields = '__all__'