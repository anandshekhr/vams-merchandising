from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = (
    [
        path(
            "accounts/reset_password/",
            auth_views.PasswordResetView.as_view(
                template_name="forgot-password.html", email_template_name="password-reset-email.html"),
            name="reset_password",
        ),
        path(
            "accounts/reset_password_sent/",
            auth_views.PasswordResetDoneView.as_view(
                template_name="password-reset-sent.html"
            ),
            name="password_reset_done",
        ),
        path(
            "accounts/reset/<uidb64>/<token>",
            auth_views.PasswordResetConfirmView.as_view(
                template_name="reset-password-form.html"
            ),
            name="password_reset_confirm_custom",
        ),
        path(
            "accounts/reset_password_complete/",
            auth_views.PasswordResetCompleteView.as_view(
                template_name="password-reset-done.html"
            ),
            name="password_reset_complete",
        ),
        path("accounts/register", views.register, name="register"),
        path("accounts/login/", views.login, name="login"),
        path("accounts/logout/", views.logout, name="logout"),
        path(
            "accounts/password/reset/",
            views.forgot_password,
            name="password-forgot-user",
        ),
        path(
            "accounts/password/reset/",
            views.password_reset_method,
            name="password-reset-web-page",
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
        path(
            "accounts/user/ordershistory/",
            views.userOrderDetail,
            name="orderhistoryuser",
        ),
        path(
            "accounts/user/ordershistory/order-detail/<int:pk>/",
            views.userOrderDetailExpanded,
            name="orderhistorydetail",
        ),
        path("accounts/register/get_otp/", views.get_otp, name="get_otp"),
        path("accounts/register/verify/", views.verify_otp, name="verify_otp"),
        path(
            "accounts/profile/dashboard/",
            views.profileDashboard,
            name="profile-dashboard",
        ),
        path("accounts/profile/address/", views.user_address, name="profile-address"),
        path(
            "accounts/profile/address/delete/<int:pk>",
            views.delete_user_address,
            name="delete-profile-address",
        ),
        path(
            "accounts/profile/address/set-primary/<int:pk>",
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
        # path('accounts/user/dashboard/',views.userDashboard,name="user-dashboard"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
