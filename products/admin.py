from django.contrib import admin
from .models import *

# Register your models here.


class ProductsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Filter products based on the logged-in user
        if not request.user.is_superuser:
            vendor = VendorDetail.objects.filter(owner=request.user)
            qs = qs.filter(vendor__in=vendor)

        return qs
    list_display: list = ('name', 'unit', 'max_retail_price',
                          'created_at', 'modified_at','vendor')
    ordering: list = ['-modified_at','-vendor','-name','-max_retail_price','-created_at']
    search_fields: list = ('name', 'material_feature',
                           'max_retail_price', 'category','vendor')


admin.site.register(Products, ProductsAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    list_display: list = ('category_id', 'category_name', 'category_image')
    search_fields: list = ('category_id', 'category_name')


admin.site.register(Categories, CategoriesAdmin)

# class ProductImagesAdmin(admin.ModelAdmin):
#     list_display: list = ('images')
#     search_fields: list = ('images','product')

admin.site.register(ProductImages)


class ProductRARAdmin(admin.ModelAdmin):
    list_display: list = ('author', 'ratings', 'review','is_approved')
    search_fields: list = ('author', 'ratings')


admin.site.register(ProductReviewAndRatings, ProductRARAdmin)


class BannersAdmin(admin.ModelAdmin):
    list_display: list = ('banner_name', 'banner_status',
                          'banner_images', 'position')
    search_fields: list = ('banner_status', 'banner_name')


admin.site.register(Banners, BannersAdmin)

# class CategoriesProductsAdmin(admin.ModelAdmin):
#     list_display: list = ('categoriesproduct_id',)
#     search_fields: list = ('categoriesproduct_id',)

admin.site.register(CategoriesProducts)


class VendorDetailAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Filter products based on the logged-in user
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)

        return qs
    list_display: list = ('storeName', 'owner', 'email',
                          'phone_number', 'address')
    ordering: list = ['-storeName', '-email', '-owner']
    search_fields: list = ('storeName', 'owner', 'email',
                           'phone_number', 'address')


admin.site.register(VendorDetail, VendorDetailAdmin)
