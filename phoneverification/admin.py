from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(DeviceOtp)
class DeviceOtpAdmin(admin.ModelAdmin):
    pass
    

    
