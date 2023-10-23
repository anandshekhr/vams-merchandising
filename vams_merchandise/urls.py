"""vams_merchandise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .settings import *
from django.contrib import admin
from django.urls import path, include, re_path,register_converter
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import PasswordResetConfirmView
from django.conf.urls import handler404, handler500
from .utils import HashIdConverter,FloatConverter

register_converter(HashIdConverter, "hashid")
register_converter(FloatConverter, "float")


admin.site.site_header = env.str('ADMIN_SITE_HEADER')
admin.site.index_title = env.str('ADMIN_INDEX_TITLE')
admin.site.site_title = env.str('ADMIN_SITE_TITLE')

urlpatterns = [
    path('', include('Home.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path("accounts/", include("dj_rest_auth.urls")),
    path("bank/", include("bankdetails.urls")),
    path("delivery/", include("delivery.urls")),
    path('user/', include('user.urls')),
    path('cart/', include('cart.urls')),
    path('seller/', include('seller.urls')),
    path('stores/', include('stores.urls')),
    path('phone/',include('phoneverification.urls')),
    path('products/', include('products.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('accounts/registration/',
         include("dj_rest_auth.registration.urls")),
    path('rest-auth/password/reset/confirm/<slug:uidb64>/<slug:token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('account/password/reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)




handler500 = 'Home.views.err_500'
