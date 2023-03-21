from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("store-detail/",StoreDetailsView.as_view()),
    path("products/",StoreProductDetailsView.as_view()),
    path("availability/", StoreVerifyAtLocation.as_view()),
    path("aboutus/",about,name="about-vams"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
