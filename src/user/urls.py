from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = (
    [
        # Login & Signup using OTP
        path("accounts/register/get_otp/", views.getOTP.as_view(), name="get_otp"),
        path("accounts/register/verify/", views.VerifyOTP.as_view(), name="verify_otp"),
        
        # login & signup using mobileno and password
        path("accounts/register", views.register, name="register"),
        path("accounts/login/", views.login, name="login"),
        path("accounts/verify/", views.verify_otp, name="verify_otp_page"),
        path("accounts/logout/", views.logout, name="logout"),
        
        # Update user information
        path(
            "accounts/update/<int:pk>",
            views.CustomerRetrieveUpdateView.as_view(),
            name="customer-retrieve-update",
        ),
        
        # reset password using email
        path(
            "accounts/reset_password/",
            auth_views.PasswordResetView.as_view(
                template_name="user/password/forgot-password.html",
                email_template_name="user/password/password-reset-email.html",
            ),
            name="reset_password",
        ),
        path(
            "accounts/reset_password_sent/",
            auth_views.PasswordResetDoneView.as_view(
                template_name="user/password/password-reset-sent.html"
            ),
            name="password_reset_done",
        ),
        path(
            "accounts/reset/<uidb64>/<token>",
            auth_views.PasswordResetConfirmView.as_view(
                template_name="user/password/reset-password-form.html"
            ),
            name="password_reset_confirm_custom",
        ),
        path(
            "accounts/reset_password_complete/",
            auth_views.PasswordResetCompleteView.as_view(
                template_name="user/password/password-reset-done.html"
            ),
            name="password_reset_complete",
        ),
        path(
            "accounts/update/user/profile/",
            views.UpdateProfileView.as_view(),
            name="auth_update_profile",
        ),
        path(
            "accounts/userprofile/",
            views.UserProfileView.as_view(),
            name="user_profile",
        ),
        path("accounts/profilepage/", views.profileUser, name="userprofilepage"),
        # User order, order-detail, profile,address, coupon, refund
        path(
            "accounts/user/ordershistory/",
            views.userOrderDetail,
            name="orderhistoryuser",
        ),
        path(
            "accounts/user/ordershistory/order-detail/<hashid:pk>/",
            views.userOrderDetailExpanded,
            name="orderhistorydetail",
        ),
        path(
            "accounts/profile/dashboard/",
            views.profileDashboard,
            name="profile-dashboard",
        ),
        path("accounts/profile/address/", views.user_address, name="profile-address"),
        path(
            "accounts/profile/address/delete/<hashid:pk>",
            views.delete_user_address,
            name="delete-profile-address",
        ),
        path(
            "accounts/profile/address/set-primary/<hashid:pk>",
            views.set_primary_address,
            name="set-primary-profile-address",
        ),
        path("accounts/profile/payment/", views.user_payment, name="profile-payments"),
        path("accounts/profile/orders/", views.user_orders, name="profile-orders"),
        path(
            "accounts/profile/notification/",
            views.user_notification,
            name="profile-notification",
        ),
        path("accounts/profile/coupon/", views.user_coupon, name="profile-coupon"),
        path(
            "accounts/profile/refund/<hashid:pk>",
            views.refund_page,
            name="refund-status",
        ),
        path(
            "accounts/user-exists/", views.UserExistView.as_view(), name="user-exists"
        ),
        path("accounts/address/", views.UserAddressAPI.as_view(), name="user-address"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
