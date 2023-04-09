from django.contrib import admin
from .models import *

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display: list = ('user','itemname','itemavailablestock','quantity','ordered')
    ordering: list = ['user']
    search_fields: list = ('user','ordered')

    def itemname(self,obj):
        return obj.item.name

    def itemavailablestock(self,obj):
        return obj.item.stock

admin.site.register(Cart,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display: list = ('user','ref_code','items_get','ordered','ordered_date','shipping_address','payment','received','refund_requested')
    ordering: list = ['user','ref_code','ordered','ordered_date','payment','refund_requested']
    search_fields: list = ('user','red_code','ordered','ordered_date','payment','refund_requested','shipping_address')

    def items_get (self,obj):
        return [item.item.name for item in obj.items.all()]
admin.site.register(Order,OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display: list =('instamojo_id','user','amount','timestamp')

admin.site.register(Payment,PaymentAdmin)
admin.site.register(DeliveryPartnerDetails)
