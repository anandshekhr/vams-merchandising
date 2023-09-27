from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, get_user_model

user = get_user_model()

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['first_name','last_name','username','email','avatar']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['images']

class ProductReviewAndRatingsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductReviewAndRatings
        fields = '__all__'
    
class ProductsSerializer(serializers.ModelSerializer):

    desc = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_desc(self,instance):
        return str(instance.desc.html)
    def get_discounted_price(self,instance):
        return instance.list_price()
    
    def get_image(self,instance):
        return instance.binaryToStringImage1()
    class Meta:
        model = Products
        fields = "__all__"
    
class BannersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banners
        fields = "__all__"

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategorySubCategories
        fields = "__all__"
        