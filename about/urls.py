from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('faq',renderFAQPage,name='faq-page'),
    path('return-policy',return_policy,name='return-policy'),
    path('refund-policy',refund_policy,name='refund-policy'),
    path('privacy-policy',privacy_policy,name='privacy-policy'),
    path('shipping-policy',shipping_and_delivery_policy,name='shipping-policy'),
    path('terms-of-service',terms_of_service_policy,name='terms-of-service'),
    path('payment-method',payment_terms_and_conditions_policy,name='payment-method'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)


