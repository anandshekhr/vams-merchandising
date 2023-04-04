import json
from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth
from rest_framework import generics, status, authentication, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
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
from django.core.paginator import Paginator


User = get_user_model()


def index(request):
    return redirect("homepage")


def homePage(request):
    try:
        products_dealoftheday = Products.objects.filter(
            category__contains=['Deal of the day'])

        products_featured = Products.objects.filter(
            category__contains=['Featured Products'])
        products_trend = Products.objects.filter(
            category__contains=['Trend Products'])
        products_best = Products.objects.filter(
            category__contains=['Best Products'])
        banners = Banners.objects.all()
        categories = Categories.objects.all()
        blog_post = Blogs.objects.all()[:3]

        # cart items for cart notification

        context = ({
            'banners': banners,
            'dealoftheday': products_dealoftheday,
            'featured': products_featured,
            'best': products_best,
            'trend': products_trend,
            'categories': categories,
            'blogs': blog_post,
        })
        return render(request, "g-2.html", context=context)
    except Exception as e:
        print(e)
        return render(request, "g-2.html")

# not using for now


def showAllProducts(request):
    products = get_object_or_404(Products)
    paginator = Paginator(products,10)
    context = {'products':products}
    return render(request,"shop-all-items.html",context)


def filter_by_category(request, category_id):
    category = Categories.objects.get(id=category_id)
    products = Products.objects.filter(
        category__contains=[category.category_name])
    data = []
    for product in products:
        data.append({
            'name': product.name,
            'description': product.desc,
            'image': product.image.url,
            'ratings': product.average_rating,
            'price': product.list_price(),
            'unit': product.unit,
            'discount': product.discount,
        })
    return JsonResponse({'products': data})

# for filter products wrt category


def seeAllProductsInCategory(request, name):
    category, created = Categories.objects.get_or_create(category_name=name)
    product = Products.objects.filter(
        category__contains=[category.category_name])
    context = {'products': product}
    return render(request, "shop-list-4.html", context)


def productDetailsPageView(request, pk):
    counter = 0
    a = 0

    # filter product for images, reviews and ratings
    product = Products.objects.get(pk=pk)
    # if ProductImages.
    image1 = ProductImages.objects.filter(product=product)[0]
    image2 = ProductImages.objects.filter(product=product)[1]
    image3 = ProductImages.objects.filter(product=product)[2]
    rating = ProductReviewAndRatings.objects.filter(
        product=product).aggregate(Avg('ratings'))
    reviews = ProductReviewAndRatings.objects.filter(product=product)

    # for greyed stars
    nonrating = 5 - int(rating['ratings__avg']
                        if rating['ratings__avg'] is not None else 0)

    # filter related products
    # category = Categories.objects.get(category_name=category_name)
    # related_products = Products.objects.filter(
    #     category__contains=[category.category_name]).exclude(pk=pk)
    # related_product_ratings = ProductReviewAndRatings.objects.filter(
    #     product__in=related_products).aggregate(Avg('ratings'))

    context = {
        'product': product,
        'image1': image1 or '',
        'image2': image2 or '',
        'image3': image3 or '',
        'rating': int(rating['ratings__avg'] or 0),
        'ratingr': [*range(int(rating['ratings__avg'] if rating['ratings__avg'] is not None else 0))],
        'nonratingr': [*range(nonrating)],
        # 'related_products': related_products,
        # 'rp_ratings': related_product_ratings or 0,
        'review': reviews,
    }

    return render(request, "shop-details.html", context)


class ProductDetailsAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, product_id, format=None):
        # product_pk = request.GET.get('product_id')
        # print(product_pk)

        # filter product for images, reviews and ratings
        product = get_object_or_404(Products, id=product_id)
        images = ProductImages.objects.filter(product=product)
        rating = ProductReviewAndRatings.objects.filter(
            product=product).aggregate(Avg('ratings'))
        listprice = product.list_price()
        review = ProductReviewAndRatings.objects.filter(product=product)

        product_serializer = ProductsSerializer(instance=product)
        images_serializer = ProductImagesSerializer(instance=images, many=True)
        review_serializer = ProductReviewAndRatingsSerializer(
            instance=review, many=True)

        nonrating = 5 - int(rating['ratings__avg']
                            if rating['ratings__avg'] is not None else 0)

        context = {
            'product': product,
            'primage': images,
            'rating': int(rating['ratings__avg'] if rating['ratings__avg'] is not None else 0),
            'ratingr': [*range(int(rating['ratings__avg'] if rating['ratings__avg'] is not None else 0))],
            'nonratingr': [*range(nonrating)],
        }

        product_html = render_to_string('product-details-modal.html', context)
        return Response({'data': product_serializer.data, 'images': images_serializer.data, 'review': review_serializer.data, 'rating': rating, 'discounted_price': listprice, 'product_html': product_html}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        pass


def searchHomePageProducts(request):
    if request.method == "GET":  # write your form name here
        product_name = request.GET.get('search')
        try:
            status = StoreProductsDetails.objects.filter(
                products__product_name__icontains=product_name)
            return render(request, "search.html", {"products": status})
        except StoreProductsDetails.DoesNotExist:
            return render(request, "search.html", {'products': status})
    else:
        return render(request, 'search.html', {'products': status})


def searchProductsInsideCategoryPage(request, pk):
    if request.method == "GET":
        product_name = request.GET.get('search')
        categorydetails = Categories.objects.get(pk=pk)
        try:
            if request.user.id != None:
                user_details = UserAddresses.objects.get(user=request.user.id)
                productdetail = StoreProductsDetails.objects.filter(products__pro_category__icontains=[
                                                                    categorydetails.category_name], products__product_name__icontains=product_name, store__storeServicablePinCodes__contains=[user_details.pincode])
                cartitems = Order.objects.get(
                    user=request.user.id, ordered=False)
                context = {'category': categorydetails,
                           'catproducts': productdetail,
                           'totalcartitem': cartitems.get_total_items_in_order() + 1,
                           'totalamount': round(cartitems.get_total(), 2),
                           'totalquantity': cartitems.get_quantity(),
                           }
            else:
                productdetail = StoreProductsDetails.objects.filter(
                    products__pro_category__icontains=[categorydetails.category_name], products__product_name__icontains=product_name)

                context = {'category': categorydetails,
                           'catproducts': productdetail,
                           'totalcartitem': 0,
                           'totalamount': 0,
                           'totalquantity': 0,
                           }
        except Order.DoesNotExist:
            context = {
                'category': categorydetails,
                'catproducts': productdetail,
                'totalcartitem': 0,
                'totalamount': 0,
                'totalquantity': 0,
            }

    return render(request, "list.html", context)


def autocompleteModel(request):
    if request.method == 'GET':
        q = request.GET.get('term', '').capitalize()
        search_qs = Products.objects.filter(product_name__startswith=q)
        results = []
        # printq
        for r in search_qs:
            results.append(r.product_name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return JsonResponse({'data': data, 'application': mimetype})


def product_detail(request, id):
    try:
        product = Products.objects.get(id=id)
        related_products = Products.objects.filter(
            category__icontains=[product.category]).exclude(id=id)[:10]

        # reviewForm = ReviewAdd()

        # Check
        canAdd = True
        reviewCheck = ProductReviewAndRatings.objects.filter(
            user=request.user, product=product).count()
        if request.user.is_authenticated:
            if reviewCheck > 0:
                canAdd = False
        # End

        # Fetch reviews
        reviews = ProductReviewAndRatings.objects.filter(product=product)
        # End

        # Fetch avg rating for reviews
        avg_reviews = ProductReviewAndRatings.objects.filter(
            product=product).aggregate(avg_rating=Avg('ratings'))
        # End
        context = {'data': product,
                   'related': related_products,
                   'canAdd': canAdd,
                   'reviews': reviews,
                   'avg_reviews': avg_reviews
                   }
        return render(request, 'product_detail.html', context)
    except:
        pass


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

# class CategoryProductsAPI(APIView):
#     permission_classes = (AllowAny,)

#     def get(self,request,pk,format =None):
#         category = Categories.objects.get(pk=pk)
#         products = Products.objects.filter(
#             category__contains=[category.category_name])
#         serializer = ProductsSerializer(instance=products,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)


class CategoryProductsAPI(generics.ListAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        queryset = Products.objects.all()
        category_id = self.request.query_params.get('pk')
        if category_id is not None:
            category = Categories.objects.get(pk=category_id)
            queryset = queryset.filter(
                category__contains=[category.category_name])
        return queryset
