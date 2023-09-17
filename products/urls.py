from django.urls import path, re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

api = settings.API_VERSION

urlpatterns = [
    path("details/<hashid:pk>/",productDetailsPageView,name="productdetail"),
    path('handle-messages/', handle_messages, name='handle_messages'),
    path("apparel/",products_list,name="show-all-products"),

    #APIs
    path("all",ProductAPI.as_view(),name="allProducts"),
    path("details/", ProductDetailsAPI.as_view(), name="allproducts"),
    path("banners/", BannersAPIView.as_view(), name="banners"),
    path("categories/", CategoriesAPI.as_view(), name="categories"),
    re_path('^category/items/(?P<pk>.+)/$',
         CategoryProductsAPI.as_view(), name="category-products-api"),
     path("reviews",ProductReviewsAPI.as_view()),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)


