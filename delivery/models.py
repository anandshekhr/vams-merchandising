from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from base64 import b64encode



# Create your models here.

class DeliveryPartnerDetail(models.Model):
    pass

    

    class Meta:
        verbose_name = _("DeliveryPartnerDetail")
        verbose_name_plural = _("DeliveryPartnerDetails")

    def __str__(self):
        return ""

    def get_absolute_url(self):
        return reverse("DeliveryPartnerDetail_detail", kwargs={"pk": self.pk})




class PincodeDetail(models.Model):
    pincode = models.IntegerField(_("Pincode"),primary_key=True)
    locality = models.CharField(_("Locality"), max_length=500,null=True,blank=True)
    city = models.CharField(_("City"), max_length=500,null=True,blank=True)
    state = models.CharField(_("State"), max_length=500,null=True,blank=True)
    can_deliver_here = models.BooleanField(_("Can Deliver Here"), default=True)
    can_pickup = models.BooleanField(_("Can Pick Up"), default=True)
    is_fraud_detected = models.BooleanField(_("Fraud Detection"), default=False)
    is_blocked = models.BooleanField(_("Blocked"), default=False)
    min_days_to_deliver = models.IntegerField(_("Min Days to Deliver"), default=4)
    max_days_to_deliver = models.IntegerField(_("Max Days to Deliver"),default=14)
    usual_days_to_deliver = models.IntegerField(_("usual Days to Deliver"),default=7)
    delivery_partners = models.ManyToManyField(DeliveryPartnerDetail)
    remarks = models.TextField(_("Remarks"),null=True,blank=True)

    class Meta:
        verbose_name = _("PincodeDetail")
        verbose_name_plural = _("PincodeDetails")

    def __str__(self):
        return self.pincode

    def get_absolute_url(self):
        return reverse("PincodeDetail_detail", kwargs={"pk": self.pk})
