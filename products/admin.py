from django.contrib import admin
from .models import *



# Register your models here.
class ProductItemForm(forms.ModelForm):
    image1 = forms.FileField(required=False)
    image2 = forms.FileField(required=False)
    image3 = forms.FileField(required=False)

    category = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'size': 10}),
    )
    subcategory = forms.ModelMultipleChoiceField(
        queryset=CategorySubCategories.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'size': 10}),
    )

    available_sizes = forms.ModelMultipleChoiceField(
        queryset=ProductSize.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'size': 10}),
    )
    tags =forms.ModelMultipleChoiceField(
        queryset=ProductTag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'size': 10}),
    )
    
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

class CategorySubCategoriesForm(forms.ModelForm):
    class Meta:
        model = CategorySubCategories
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategorySubCategoriesForm, self).__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = CategorySubCategories.objects.filter(category=category_id)
            except (ValueError, TypeError):
                pass  # Invalid input from the form; ignore and use the default queryset

@admin.register(CategorySubCategories)
class CategorySubCategoriesAdmin(admin.ModelAdmin):
    
    list_display: list = ('category_name','subcategory')
    search_fields: list = ('category_name','subcategory')

class ProductSizeForm(forms.ModelForm):
    subcategory = forms.ModelMultipleChoiceField(
        queryset=CategorySubCategories.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'size': 10}),
    )
@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    form = ProductSizeForm
    list_display: list = ('subCategoryName','name','code')
    search_fields: list = ('subCategoryName','name','code')
    ordering: list = ['-name','-code']

class ProductTagForm(forms.ModelForm):
    subcategory = forms.ModelMultipleChoiceField(
        queryset=CategorySubCategories.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'size': 10}),
    )

@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    form = ProductTagForm
    list_display: list = ('subCategoryName','name','code')
    search_fields: list = ('subCategoryName','name','code')
    ordering: list = ['-name','-code']

    


    

class ProductsAdmin(admin.ModelAdmin):
    form = ProductItemForm
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['slug'].widget.attrs['placeholder'] = "Enter Slug in this format: brand-size-color-productname"
        form.base_fields['name'].widget.attrs['placeholder'] = "Enter product name"
        form.base_fields['longname'].widget.attrs['placeholder'] = "Enter product name with some details"
        form.base_fields['name'].widget.attrs['placeholder'] = "Enter product name"
        form.base_fields['desc'].widget.attrs['placeholder'] = "Enter product description here"
        form.base_fields['unit'].widget.attrs['placeholder'] = "Enter unit as e.g. 'Pack of 1'"
        form.base_fields['brand'].widget.attrs['placeholder'] = "Enter product brand here"

        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Filter products based on the logged-in user
        if not request.user.is_superuser:
            vendor = VendorDetail.objects.filter(owner=request.user)
            qs = qs.filter(vendor__in=vendor)

        return qs

    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to save the object
        super().save_model(request, obj, form, change)
        
        # Get the selected categories from the form
        selected_categories = form.cleaned_data['category']
        selected_subcategories = form.cleaned_data['subcategory']
        selected_sizes = form.cleaned_data['available_sizes']
        selected_tags  = form.cleaned_data['tags']

        # Clear existing categories for the object
        obj.category.clear()
        obj.subcategory.clear()
        obj.available_sizes.clear()
        obj.tags.clear()

        # Add the selected categories to the object
        for category in selected_categories:
            obj.category.add(category)

        for scategory in selected_subcategories:
            obj.subcategory.add(scategory)
        
        for asizes in selected_sizes:
            obj.available_sizes.add(asizes)
        
        for tag in selected_tags:
            obj.tags.add(tag)

        # Save the object
        obj.save()

    list_display: list = ('scheme_image_tag','name', 'unit', 'sizes','stock','max_retail_price','discount','list_price',
                          'vendor','created_at')
    ordering: list = ['-modified_at','-vendor','-name','-max_retail_price','-created_at']
    search_fields: list = ('name', 'material_feature',
                           'max_retail_price', 'category','vendor')


admin.site.register(Products, ProductsAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    list_display: list = ('category_id', 'category_name')
    search_fields: list = ('category_id', 'category_name')


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(ProductImages)

class ProductRARAdmin(admin.ModelAdmin):
    list_display: list = ('author', 'ratings', 'review','is_approved')
    search_fields: list = ('author', 'ratings')

admin.site.register(ProductReviewAndRatings, ProductRARAdmin)

class BannerItemForm(forms.ModelForm):
    banner_images = forms.FileField(required=False)
    banner_product_category = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'size': 10}),
    )
    

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

    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to save the object
        super().save_model(request, obj, form, change)
        
        # Get the selected categories from the form
        banner_product_category = form.cleaned_data['banner_product_category']
        

        # Clear existing categories for the object
        obj.banner_product_category.clear()
        

        # Add the selected categories to the object
        for category in banner_product_category:
            obj.banner_product_category.add(category)

        # Save the object
        obj.save()
    list_display: list = ('scheme_image_tag','banner_name', 'banner_status',
                           'position')
    search_fields: list = ('banner_status', 'banner_name')


admin.site.register(Banners, BannersAdmin)

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

    

