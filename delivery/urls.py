from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('pincode/get/', PincodeListCreateView.as_view(), name='seller-list-create'),
    path('pincode/update/<int:pk>', PincodeRetrieveUpdateView.as_view(), name='seller-retrieve-update'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)
