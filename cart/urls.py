from django.urls import path,register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .utils import FloatConverter

# register_converter(converters.RomanNumeralConverter, 'roman')
register_converter(FloatConverter, 'float')

urlpatterns = [
    path("addtocart/<int:pk>/<str:size>", addToCart, name="addtocart"),
    path("cart/add/<int:pk>", addToCartWithSizeQuantity,name="add-to-cart-size-qty"),
    path("ordersummary/",cartCheckoutPageView,name="cartview"),
    path("checkout/",checkoutPage,name="payment-checkout"),
    path("removesingleitemfromcart/<int:pk>",removeSingleItemFromCart,name="removesingleitemfromcart"),
    path("payment/checkout/<float:amount>",orderPaymentRequest,name="paymentcheckout"),
    path("paymentstatusupdate/",paymentStatusAndOrderStatusUpdate,name="paymentstatusupdate"),
    path("cart/delete/item/<int:pk>",deleteItemFromCart,name="delete-from-cart"),
    path("order-summary/<int:pk>/", order_summary, name="ordersummary"),
    path("payment-pending/<int:pk>/",
         pending_payment_page, name="pending-payment"),
    path("payment-failed/<int:pk>/",
         failed_payment_page, name="failed-payment"),
    path("cart/move-to-cart/<int:pk>", moveToCart,name="move-to-cart"),

     # api
     path("customer/order/add/", CartAddView.as_view(),name="order-add-api"),
     path("customer/order/remove/",CartRemoveView.as_view(),name="order-remove-api"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)


