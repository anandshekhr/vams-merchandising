# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import CurrentUserDefault
from .models import *
try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

User = get_user_model()

class LoginOTPSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=10)
    mobile = serializers.CharField(max_length=10)
    otp = serializers.CharField(
        label=_("otp"),
        style={'input_type': 'otp'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        country_code = data.get('country_code')
        mobile = data.get('phone_number')
        otp = data.get('otp')
        country_id = Country.objects.get(country_code=country_code)
        device_otp = DeviceOtp.objects.get(
            number=mobile, status=True, country=country_id)

        if mobile and device_otp and int(otp) == device_otp.otp:
            user = authenticate(request=self.context.get('request'),
                                mobile=mobile)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('OTP Mismatched.')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data