from django.contrib import admin
from .models import *

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display: list = ('user','itemname','itemavailablestock','quantity','ordered','created_at','modified_at')
    ordering: list = ['user']
    search_fields: list = ('user','ordered')

    def itemname(self,obj):
        return obj.item.name

    def itemavailablestock(self,obj):
        return obj.item.stock

admin.site.register(Cart,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display: list = ('user','ref_code','items_get','ordered','ordered_date','shipping_address','payment','refund_requested')
    ordering: list = ['user','ref_code','ordered','ordered_date','payment','refund_requested']
    search_fields: list = ('user','red_code','ordered','ordered_date','payment','refund_requested','shipping_address')

    def items_get (self,obj):
        return [item.item.name for item in obj.items.all()]
admin.site.register(Order,OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display: list =('instamojo_id','user','amount','timestamp')

admin.site.register(Payment,PaymentAdmin)
admin.site.register(DeliveryPartnerDetails)


@admin.register(VendorOrderDetail)
class VendorOrderDetailAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Filter products based on the logged-in user
        if not request.user.is_superuser:
            vendor = VendorDetail.objects.filter(owner=request.user)
            qs = qs.filter(vendor__in=vendor)

        return qs
    list_display: list = ('vendor', 'order_id', 'order_item',
                          'order_item_size','order_item_qty','order_amount','payment_status','order_packed','order_shipped')
    ordering: list = ['vendor', 'order_id', 'order_item',
                          'order_item_size','order_item_qty','order_amount','payment_status','order_packed','order_shipped']
    search_fields: list = ('vendor__storeName','order_id', 'order_item__name',
                          'order_item_size','order_item_qty','order_amount','payment_status','order_packed','order_shipped')
    
@admin.register(VendorTransactionDetail)
class VendorTransactionDetailAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Filter products based on the logged-in user
        if not request.user.is_superuser:
            vendor = VendorDetail.objects.filter(owner=request.user)
            qs = qs.filter(vendor__in=vendor)

        return qs
    list_display: list = ('vendor', 'order_id', 'order_receiving_date',
                          'total_order_amount','order_completed_date','payment_status','payment_transfer_date')
    ordering: list = ['vendor', 'order_id', 'order_receiving_date',
                          'total_order_amount','order_completed_date','payment_status','payment_transfer_date']
    search_fields: list = ('vendor__storeName', 'order_id', 'order_receiving_date',
                          'total_order_amount','order_completed_date','payment_status','payment_transfer_date')
    

admin.site.register(Refund)
admin.site.register(UserBankAccount)