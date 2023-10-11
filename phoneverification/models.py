from django.db import models
from datetime import date
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

class Country(models.Model):
    country_code = models.CharField(max_length=4, blank=True, null=True)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    nick_name = models.CharField(max_length=5, blank=True, null=True)
    country_image = models.CharField(max_length=200, blank=True, null=True)
    country_image_2 = models.ImageField(upload_to='country', null=True)
    is_top = models.BooleanField(_('is_top'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)

    def __str__(self):
        return self.country_name


class DeviceOtp(models.Model):
    country = models.ForeignKey(
        Country, related_name='device_country_user', on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=50, blank=False, null=False)
    otp = models.IntegerField(blank=True, null=True, default=0)
    session = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False)
    auth_token = models.UUIDField(
        _("auth_token"), null=True, blank=True, default=uuid.uuid4)
    created_date = models.DateTimeField('date created', auto_now_add=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return self.number