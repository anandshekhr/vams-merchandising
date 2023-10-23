from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(PaymentsEmails)
class PaymentsEmailsAdmin(admin.ModelAdmin):
    pass
@admin.register(UserRegisteredEmails)
class UserRegisteredEmailsAdmin(admin.ModelAdmin):
    pass

@admin.register(DelayDeliveryAndRefundEmails)
class DelayDeliveryAndRefundEmailsAdmin(admin.ModelAdmin):
    pass

@admin.register(PromotionalEmails)
class PromotionalEmailsAdmin(admin.ModelAdmin):
    pass
    

    

    

    
