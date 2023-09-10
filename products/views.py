import json
from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth,messages
from rest_framework import generics, status, authentication, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.views.generic import *
from user.models import *
from stores.models import *
from cart.models import *
from django.http import JsonResponse
from django.db.models import Max, Min, Count, Avg
from django.template.loader import render_to_string
from blogs.models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters,pagination
from django_filters import FilterSet


User = get_user_model()
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

# adding filters to API
class ProductsFilter(FilterSet):
    def filter_queryset(self, request, queryset, view):
        category_value = request.query_params.get("category")
        sizes_value = request.query_params.get("available_sizes")
        tags_value = request.query_params.get("tags")
        ratings_value = request.query_params.get("average_rating")
        brand = request.query_params.get("brand")
        price_begin = request.query_params.get("price_begin")
        price_end = request.query_params.get("price_end")



        if category_value:
            queryset = queryset.filter(category__contains=category_value.split(','))

        if sizes_value:
            queryset = queryset.filter(available_sizes__contains__in=sizes_value)

        if tags_value:
            queryset = queryset.filter(tags__contains=tags_value.split(','))
        
        if ratings_value:
            queryset = queryset.filter(average_rating__contains=str(ratings_value))
        
        if brand:
            queryset = queryset.filter(brand__icontains=str(brand))
        
        if price_begin or price_end:
            queryset = queryset.filter(max_retail_price__range=[str(price_begin),str(price_end)])

        return queryset

    class Meta:
        model = Products
        fields = (
            "subcategory",
        )

def showAllProducts(request):
    products = Products.objects.all()
    # paginator = Paginator(products, 10)
    context = {"products": products}
    return render(request, "shop.html", context)

def handle_messages(request):
    message_type = request.GET.get('type')
    
    message = request.GET.get('message')
    

    if message_type and message:
        if message_type == 'success':
            messages.success(request, message)
        elif message_type == 'error':
            messages.error(request, message)

    return JsonResponse({'status': 'ok'})

def productDetailsPageView(request, pk):
    counter = 0
    a = 0

    # filter product for images, reviews and ratings
    product = Products.objects.get(pk=pk)
    rating = ProductReviewAndRatings.objects.filter(product=product).aggregate(
        Avg("ratings")
    )
    reviews = ProductReviewAndRatings.objects.filter(product=product, is_approved=True)
    total_reviews_count = reviews.count()
    related_products = Products.objects.filter(category__contains=[product.category[0]])

    # for greyed stars
    nonrating = 5 - int(
        rating["ratings__avg"] if rating["ratings__avg"] is not None else 0
    )
    context = {
        "total_stars": range(5),
        "product": product,
        "rating": int(rating["ratings__avg"] or 0),
        "ratingr": [
            *range(
                int(rating["ratings__avg"] if rating["ratings__avg"] is not None else 0)
            )
        ],
        "nonratingr": [*range(nonrating)],
        "reviews": reviews,
        "related_products": related_products,
        "total_reviews_count":total_reviews_count,
    }

    return render(request, "shop-details.html", context)


class ProductAPI(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ProductsFilter]
    search_fields = ["id", "name", "longname", "desc", "brand", "tags", "discount"]
    permission_classes = (AllowAny,)
    # pagination_class = [StandardResultsSetPagination]
    # authentication_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailsAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        product_id = request.data.get('id')
        
        # filter product for images, reviews and ratings
        product = get_object_or_404(Products, id=product_id)
        images = ProductImages.objects.filter(product=product)
        rating = ProductReviewAndRatings.objects.filter(product=product).aggregate(
            Avg("ratings")
        )
        listprice = product.list_price()
        review = ProductReviewAndRatings.objects.filter(product=product)

        product_serializer = ProductsSerializer(instance=product)
        images_serializer = ProductImagesSerializer(instance=images, many=True)
        review_serializer = ProductReviewAndRatingsSerializer(
            instance=review, many=True
        )

        nonrating = 5 - int(
            rating["ratings__avg"] if rating["ratings__avg"] is not None else 0
        )

        context = {
            "product": product,
            "primage": images,
            "rating": int(
                rating["ratings__avg"] if rating["ratings__avg"] is not None else 0
            ),
            "ratingr": [
                *range(
                    int(
                        rating["ratings__avg"]
                        if rating["ratings__avg"] is not None
                        else 0
                    )
                )
            ],
            "nonratingr": [*range(nonrating)],
        }

        # product_html = render_to_string("product-details-modal.html", context)
        return Response(
            {
                "data": product_serializer.data,
                "images": images_serializer.data,
                "review": review_serializer.data,
                "rating": rating,
                "discounted_price": listprice,
                # "product_html": product_html,
            },
            status=status.HTTP_200_OK,
        )

class BannersAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        banners = Banners.objects.all()
        serializer = BannersSerializer(instance=banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoriesAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(instance=categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryProductsAPI(generics.ListAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        queryset = Products.objects.all()
        category_id = self.request.query_params.get("pk")
        if category_id is not None:
            category = Categories.objects.get(pk=category_id)
            queryset = queryset.filter(category__contains=[category.category_name])
        return queryset

class ProductReviewsAPI(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, *args, **kwargs):
        queryset = ProductReviewAndRatings.objects.all()
        serializer = ProductReviewAndRatingsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProductReviewAndRatingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def products_list(request):
    # Get filter options from request (e.g., category)
    category = request.GET.get('category')
    size = request.GET.get('size')
    web = request.GET.get('web')
    page = request.GET.get('page')
    ratings = request.GET.get('ratings')
    discount = request.GET.get('discount')
    brand = request.GET.get('brand')
    price = request.GET.get('price')

    
    
    # Retrieve all products or filter by category
    products = Products.objects.all()
    if category:
        products = products.filter(subcategory=category)
    
    if size:
        size = size.split(',')
        products = products.filter(available_sizes__contains=size)
    
    if ratings != "None" and ratings != None:
        products = products.filter(average_rating=ratings) 
    
    if discount != "0.0" and discount != None:
        discount_1 = float(discount.split(' TO ')[0])
        discount_2 = float(discount.split(' TO ')[1])
        products = products.filter(discount__range=[discount_1,discount_2])
    
    if brand:
        brand = brand.split(',')
        products = products.filter(brand__contains=brand)
    
    if price:
        price = price.split(',')
        products = products.filter(max_retail_price__range = price)


    # Paginate the products
    paginator = Paginator(products, 24)
    
    try:
        product_page = paginator.get_page(page)
    except PageNotAnInteger:
        product_page = paginator.page(1)
    except EmptyPage:
        product_page = paginator.page(paginator.num_pages)

    # Generate HTML for product list and pagination
    product_list_html = render(request, 'shop/products.html', {'products': product_page})
    pagination_html = render(request, 'shop/pagination.html', {'products': product_page, 'page': page})
    product_list_pagination_html = render(request, 'shop/product-list.html',{'products':product_page})

    if web:
        # If it's an AJAX request, return JSON response
        return JsonResponse({
            'product_list': product_list_html.content.decode(),
            'pagination': pagination_html.content.decode(),
            'pagination_product_list':product_list_pagination_html.content.decode(),
        })
    else:
        context = {'products': product_page}
        # For regular requests, return the HTML template
        return render(request, 'shop.html', context=context)
