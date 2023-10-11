from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('register/', SellerListCreateView.as_view(), name='seller-list-create'),
    path('update/<int:pk>', SellerRetrieveUpdateView.as_view(), name='seller-retrieve-update'),
    path('store/register/', SellerStoreDetailsListCreateView.as_view(), name='seller-store-list-create'),
    path('store/update/<int:pk>', SellerStoreDetailsRetrieveUpdateView.as_view(), name='seller-store-retrieve-update'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)

