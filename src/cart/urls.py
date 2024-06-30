from django.urls import path,register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
     path("viewcart/",cartCheckoutPageView,name="cartview"),
     path("addtocart/<hashid:pk>/<hashid:size>", addToCart, name="addtocart"),
     path("update/items/add/<hashid:pk>", addToCartWithSizeQuantity,name="add-to-cart-size-qty"),
     path("remove/item/qty/<hashid:pk>",removeSingleItemFromCart,name="removesingleitemfromcart"),
     path("delete/item/<hashid:pk>",deleteItemFromCart,name="delete-from-cart"),

     path("checkout/",checkoutPage,name="payment-checkout"),
     path("payment/instamojo/checkout/<float:amount>",orderPaymentRequestInstamojo,name="payment-checkout-instamojo"),
     path("payment/phonepe/checkout/<float:amount>",orderPaymentRequestPhonePe,name="payment-checkout-phonepe"),
     
     path('payment/razorpay/success/',razorpay_success_redirect,name="razorpay-payment-success"),
     path("payment/instamojo/success/",paymentStatusAndOrderStatusUpdate,name="payment-status-update"),
     path("payment/phonepe/success/",paymentStatusAndOrderStatusUpdatePhonePe,name="payment-status-update-phonepe"),

     path("payment/instamojo/pending/<hashid:pk>/",pending_payment_page, name="pending-payment"),
     path("payment/instamojo/failed/<hashid:pk>/",failed_payment_page, name="failed-payment"),
     
     path("success/thankyou/<hashid:pk>/", order_summary, name="ordersummary"),
     
     # api
     path("move-to-cart/", moveToCart.as_view(),name="move-to-cart"),
     path("customer/order/add/", CartAddView.as_view(),name="order-add-api"),
     path("customer/order/remove/",CartRemoveView.as_view(),name="order-remove-api"),
     path("payment/phonepe/success/callback/",PhonePePaymentCallbackAPI,name='success-callback-phonepe')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)


