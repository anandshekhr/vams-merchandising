from django.urls import path, re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('send-otp/', get_otp, name='get_otp'),
    path('verify/', verify_otp, name='verify_otp'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)
