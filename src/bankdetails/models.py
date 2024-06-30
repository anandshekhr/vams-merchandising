from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ifscCodeDetails(models.Model):
    bank = models.CharField(_("Bank"), max_length=500)
    ifsc = models.CharField(_("IFSC"), max_length=50)
    micr = models.CharField(_("MICR Code"), max_length=50,null=True, blank=True)
    branch = models.CharField(_("Branch"), max_length=100,null=True, blank=True)
    address = models.TextField(_("Address"),null=True, blank=True)
    city1 = models.CharField(_("City1"), max_length=50,null=True, blank=True)
    city2 = models.CharField(_("City2"), max_length=50,null=True, blank=True)
    state = models.CharField(_("State"), max_length=100,null=True, blank=True)
    std_code = models.CharField(_("Std Code"), max_length=50,null=True, blank=True)
    contact = models.CharField(_("Contact"), max_length=50,null=True, blank=True)
    active = models.BooleanField(_("Active"),default=True)
    created_at = models.DateTimeField(_("Created Date"), auto_now_add=True,null=True, blank=True)
    modified_at = models.DateTimeField(_("Modified Date"), auto_now=True,null=True, blank=True)
    bank_code = models.CharField(_("Bank Code"), max_length=10,default="",null=True, blank=True)
    rtgs = models.BooleanField(_("RTGS"), default=True)

    class Meta:
        verbose_name = _("ifscCodeDetail")
        verbose_name_plural = _("ifscCodeDetails")

    def __str__(self):
        return self.bank

    def get_absolute_url(self):
        return reverse("ifscCodeDetail_details", kwargs={"pk": self.pk})
