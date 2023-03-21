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
    author = userSerializer()
    class Meta:
        model = ProductReviewAndRatings
        fields = ['review','ratings','upload_image','author']
    
class ProductsSerializer(serializers.ModelSerializer):

    desc = serializers.SerializerMethodField()

    def get_desc(self,instance):
        return str(instance.desc.html)
    class Meta:
        model = Products
        fields = "__all__"
    
class BannersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banners
        fields = "__all__"
