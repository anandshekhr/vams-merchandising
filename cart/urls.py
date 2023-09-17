from django.urls import path,register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("addtocart/<hashid:pk>/<hashid:size>", addToCart, name="addtocart"),
    path("cart/add/<hashid:pk>", addToCartWithSizeQuantity,name="add-to-cart-size-qty"),
    path("ordersummary/",cartCheckoutPageView,name="cartview"),
    path("checkout/",checkoutPage,name="payment-checkout"),
    path("removesingleitemfromcart/<hashid:pk>",removeSingleItemFromCart,name="removesingleitemfromcart"),
    path("payment/checkout/<float:amount>",orderPaymentRequest,name="paymentcheckout"),
    path("paymentstatusupdate/",paymentStatusAndOrderStatusUpdate,name="paymentstatusupdate"),
    path("cart/delete/item/<hashid:pk>",deleteItemFromCart,name="delete-from-cart"),
    path("order-summary/<hashid:pk>/", order_summary, name="ordersummary"),
    path("payment-pending/<hashid:pk>/",
         pending_payment_page, name="pending-payment"),
    path("payment-failed/<hashid:pk>/",
         failed_payment_page, name="failed-payment"),

     # api
     path("move-to-cart/", moveToCart.as_view(),name="move-to-cart"),
     path("customer/order/add/", CartAddView.as_view(),name="order-add-api"),
     path("customer/order/remove/",CartRemoveView.as_view(),name="order-remove-api"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)


