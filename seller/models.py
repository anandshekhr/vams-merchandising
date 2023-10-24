from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import Country

# Create your models here.
class Seller(models.Model):
    name = models.CharField(_("Name"), max_length=50, blank=True,null=True)
    country = models.ForeignKey(Country, verbose_name=_("Country"), on_delete=models.CASCADE, blank=True,null=True)
    phone = models.CharField(_("Phone"), max_length=10, blank=True,null=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True,null=True)
    password = models.CharField(_("Password"), max_length=2000, blank=True,null=True)

    class Meta:
        verbose_name = _("Seller")
        verbose_name_plural = _("Sellers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Seller_detail", kwargs={"pk": self.pk})


class SellerStoreDetails(models.Model):
    seller = models.ForeignKey(Seller, verbose_name=_("Seller"), on_delete=models.CASCADE)
    gst = models.CharField(_("GST No."), max_length=50, blank=True, null=True)
    name = models.CharField(_("Store Name"), max_length=200, blank=True, null=True)
    address = models.TextField(_("Store Address"),null=True,blank=True)

    class Meta:
        verbose_name = _("SellerStoreDetails")
        verbose_name_plural = _("SellerStoreDetailss")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("SellerStoreDetails_detail", kwargs={"pk": self.pk})
