from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, get_user_model
from datetime import datetime, timedelta
user = get_user_model()

class PincodeDetailSerializer(serializers.ModelSerializer):
    delivery_by = serializers.SerializerMethodField()
    class Meta:
        model = PincodeDetail
        fields = '__all__'
    
    def get_delivery_by(self,instance):
        usual_delivery_date = instance.usual_days_to_deliver
        current_datetime = datetime.now()
        delivery_by = current_datetime +timedelta(days=usual_delivery_date)
        day = delivery_by.strftime("%A")
        date = delivery_by.strftime("%b %d")
        return f"Get it by {day}, {date}"