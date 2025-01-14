from django.contrib import admin
from .models import *
# Register your models here.
class StoreProductsAdmin(admin.ModelAdmin):
    list_display: list = ('pname','unit','mrp','ourprice','available_stock','storename')
    ordering: list = ['-available_stock']
    search_fields: list = ('storeAddress','products','available_stock')

    def storeAddress(self,obj):
        return obj.store.fullStoreAddress()
    
    def mrp(self,obj):
        return obj.products.max_retail_price
    
    def unit(self,obj):
        return obj.products.unit
    
    def pname(self,obj):
        return obj.products.name
    
    def ourprice(self,obj):
        list_price = obj.products.list_price()
        return list_price

    def storename(self,obj):
        return obj.store.storeName
admin.site.register(StoreProductsDetails,StoreProductsAdmin)

class StoreDetailsAdmin(admin.ModelAdmin):
    list_display: list = ('storeName','fullStoreAddress','storeEmail','storePhoneNo','storeRating','storeStatus','storeServicablePinCodes',)
    ordering: list = ['-storeLocalityPinCode']
    search_fields: list = ('storeName','storeLocalityPinCode','storeServicablePinCodes','storeRating','storeStatus')

admin.site.register(StoreDetail,StoreDetailsAdmin)

admin.site.register(PoliciesDetails)
admin.site.register(FAQ)


