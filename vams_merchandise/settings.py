"""
Django settings for vams_merchandise project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

admin_volt = "admin_volt.apps.AdminVoltConfig"

# Application definition
INSTALLED_APPS = [
    # admin_volt,  # Make sure 'admin_volt' is a string or variable
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "django.contrib.sites",
    "django_rest_passwordreset",
    "about.apps.AboutConfig",
    "Home.apps.HomeConfig",
    "user.apps.AccountConfig",
    "products.apps.ProductsConfig",
    "stores.apps.StoresConfig",
    "cart.apps.CartConfig",
    "blogs.apps.BlogsConfig",
    "wishlist.apps.WishlistConfig",
    "bankdetails.apps.BankdetailsConfig",
    "phoneverification.apps.PhoneverificationConfig",
    "seller.apps.SellerConfig",
    "delivery.apps.DeliveryConfig",
    "emailapp.apps.EmailappConfig",

    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.apple",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth.registration",
    "django_quill",
    "django_filters",
    "django_celery_results",
    "django_celery_beat"]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "vams_merchandise.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "Home.customBaseVariable.addVariableBaseTemplate",
            ],
            "libraries": {
                "range": "products.templatetags.range",
            },
        },
    },
]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SITE_ID = 1

WSGI_APPLICATION = "vams_merchandise.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "vamscentral2",
            "USER": "postgres",
            "PASSWORD": "prune",
            "HOST": "localhost",
            "PORT": "5433",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DATABASE_NAME"),
            "USER": env("DATABASE_USERNAME"),
            "PASSWORD": env("PASSWORD"),
            "HOST": env("DATABASE_URL"),
            "PORT": env("DATABASE_PORT"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Calcutta"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
if DEBUG:
    STATIC_URL = "static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_DIRS = [BASE_DIR / "static"]
else:
    STATIC_URL = "static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [  # new
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

AUTH_USER_MODEL = env.str("AUTH_USER_MODEL")
REST_AUTH_SERIALIZERS = {"LOGIN_SERIALIZER": "user.serializers.LoginSerializer"}
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "user.serializers.RegisterSerializer"
}
ACCOUNT_AUTHENTICATION_METHOD = env("ACCOUNT_AUTHENTICATION_METHOD")
ACCOUNT_USERNAME_REQUIRED = env("ACCOUNT_USERNAME_REQUIRED")
ACCOUNT_EMAIL_REQUIRED = env("ACCOUNT_EMAIL_REQUIRED")
ACCOUNT_UNIQUE_EMAIL = env("ACCOUNT_UNIQUE_EMAIL")
ACCOUNT_EMAIL_VERIFICATION = env("ACCOUNT_EMAIL_VERIFICATION")
ACCOUNT_ADAPTER = "user.adapters.CustomUserAccountAdapter"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# INSTAMOJO API DETAILS
API_KEY = env("INSTAMOJO_API_KEY")
AUTH_TOKEN = env("INSTAMOJO_AUTH_TOKEN")
API_SALT = env("INSTAMOJO_API_SALT")
PAYMENT_SUCCESS_REDIRECT_URL = env("PAYMENT_SUCCESS_REDIRECT_URL")
SEND_SMS = env("INSTAMOJO_SEND_PAYMENT_RECEIVED_SMS")
SEND_EMAIL = env("INSTAMOJO_SEND_PAYMENT_RECEIVED_EMAIL")
ENDPOINT = env("INSTAMOJO_TEST_ENDPOINT")

API_VERSION = env("API_VERSION")

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# CELERY_BACKENDS
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

CELERY_RESULT_BACKEND = 'django-db'

# celery beat
CELERY_BEAT_SCHEDULER ='django_celery_beat.schedulers:DatabaseSchedulers'

# Email server for reset password
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-mail.outlook.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "vamscentral@hotmail.com"
EMAIL_HOST_PASSWORD = "1$Onemanarmy$2023"
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "www.vamscentral.com <vamscentral@hotmail.com>"

ADMIN_EMAIL = "shekharanand7773@gmail.com"



# GST
GST_STICHED = 12

# Delivery Charges
DELIVERY = 40
ABOVE_AMOUNT = 600


# Hashing 
HASHIDS_SALT = 'jkqbdvaiacobaowr27834691230jnfbqoey92tribhwefq8w9r1@E23jr23r!3hrg81t43r1r'


# razorpay test mode
RAZORPAY_API_KEY = env('RAZORPAY_API_KEY')
RAZORPAY_API_KEY_SECRET = env('RAZORPAY_API_KEY_SECRET')

# Infobip whatsapp information
SENDER_PHONE_NUMBER = env('SENDER_PHONE_NUMBER')
IB_API_KEY = env('INFOBIP_API_KEY')
IB_BASE_URL = env('INFOBIP_BASE_URL')