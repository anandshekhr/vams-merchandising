from django.contrib import admin
from .models import *

# Register your models here.

class ProductItemForm(forms.ModelForm):
    image1 = forms.FileField(required=False)
    image2 = forms.FileField(required=False)
    image3 = forms.FileField(required=False)

    def save(self, commit=True):
        if self.cleaned_data.get('image1') is not None \
                and hasattr(self.cleaned_data['image1'], 'file'):
            data = self.cleaned_data['image1'].file.read()
            self.instance.image1 = data
        
        if self.cleaned_data.get('image2') is not None and hasattr(self.cleaned_data['image2'], 'file'):
            data = self.cleaned_data['image2'].file.read()
            self.instance.image2 = data
        
        if self.cleaned_data.get('image3') is not None and hasattr(self.cleaned_data['image3'], 'file'):
            data = self.cleaned_data['image3'].file.read()
            self.instance.image3 = data

        return self.instance

    def save_m2m(self):
        # FIXME: this function is required by ModelAdmin, otherwise save process will fail
        pass

class ProductsAdmin(admin.ModelAdmin):
    form = ProductItemForm
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Filter products based on the logged-in user
        if not request.user.is_superuser:
            vendor = VendorDetail.objects.filter(owner=request.user)
            qs = qs.filter(vendor__in=vendor)

        return qs
    list_display: list = ('name', 'unit', 'max_retail_price',
                          'created_at', 'modified_at','vendor','scheme_image_tag')
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

class BannerItemForm(forms.ModelForm):
    banner_images = forms.FileField(required=False)
    

    def save(self, commit=True):
        if self.cleaned_data.get('banner_images') is not None \
                and hasattr(self.cleaned_data['banner_images'], 'file'):
            data = self.cleaned_data['banner_images'].file.read()
            self.instance.banner_images = data

        return self.instance

    def save_m2m(self):
        # FIXME: this function is required by ModelAdmin, otherwise save process will fail
        pass
class BannersAdmin(admin.ModelAdmin):
    form = BannerItemForm
    list_display: list = ('banner_name', 'banner_status',
                          'scheme_image_tag', 'position')
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
    ordering: list = ['-storeName', '-email', '-owner','-phone_number']
    search_fields: list = ('storeName', 'owner', 'email',
                           'phone_number', 'address')


admin.site.register(VendorDetail, VendorDetailAdmin)

@admin.register(VendorBankAccountDetail)
class VendorBankAccountDetailAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Filter products based on the logged-in user
        if not request.user.is_superuser:
            vendor = VendorDetail.objects.filter(owner=request.user)
            qs = qs.filter(vendor__in=vendor)

        return qs
    list_display: list = ('vendor', 'bank_name', 'bank_account_number',
                          'ifsc_code')
    ordering: list = ['-vendor', '-bank_name', '-bank_account_number',
                          '-ifsc_code']
    search_fields: list = ('vendor', 'bank_name', 'bank_account_number',
                          'ifsc_code')

    

