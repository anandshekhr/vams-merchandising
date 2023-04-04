from django.urls import path, re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

api = settings.API_VERSION

urlpatterns = [
    path("home/", homePage, name="homepage"),
    path("categories/<str:name>", seeAllProductsInCategory,
         name="seeallproductsincategory"),
    path("details/<int:pk>/",productDetailsPageView,name="productdetail"),
    path("search?name=", autocompleteModel, name="productsearch"),
    path("categories/search/<int:pk>",searchProductsInsideCategoryPage,name="productsearchcategory"),
    path("category/products?<int:category_id>", filter_by_category,name="filter_by_category"),
    path("products/show-all/",showAllProducts,name="show-all-products"),

    #APIs
    path("details/id=<int:product_id>", ProductDetailsAPI.as_view(), name="allproducts"),
    path("banners/", BannersAPIView.as_view(), name="banners"),
    path("categories/", CategoriesAPI.as_view(), name="categories"),
    re_path('^category/items/(?P<pk>.+)/$',
         CategoryProductsAPI.as_view(), name="category-products-api"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
