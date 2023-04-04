from django.urls import path,register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from cart.utils import FloatConverter

# register_converter(converters.RomanNumeralConverter, 'roman')
register_converter(FloatConverter, 'float')

urlpatterns = [
        path("wishlist/<int:pk>/",addToWishlist,name="add-to-wishlist"),
        path("wishlist/",wishlistView,name="wishlist-view"),
        path("wishlist/delete/item/<int:pk>",deleteItemFromWishlist,name="delete-item-from-wishlist"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)