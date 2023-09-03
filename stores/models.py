from django.db import models
from django.urls import reverse
from products.models import * 
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.contrib.postgres.fields import ArrayField


# Create your models here.
RATINGS = ((1,1),(2,2),(3,3),(4,4),(5,5),)

class StoreDetail(models.Model):
    storeName = models.CharField(_("Store Name"), max_length=50,null=False,default="")
    storeAddress = models.CharField(_("Store Address"), max_length=250,null=False,default="",blank=False)
    storeLocality = models.CharField(_("Store Locality"), max_length=50,null=False,default= "",blank=False)
    storeLocalityPinCode = models.IntegerField(_("Store Locality Pincode"),null=True,blank=True)
    storeServicablePinCodes = ArrayField(models.CharField(_("Store Servicable Pincodes"), max_length=2048,default="",null=True,blank=True),null=True,blank=True)
    storePhoneNo = models.CharField(_("Store Phone No."),max_length=15,null=True,blank=True)
    storeEmail = models.EmailField(_("Store Email ID"), max_length=254,null= True,blank=True)
    storeRating = models.IntegerField(_("Store Rating"),choices=RATINGS,null=True,blank=True)
    storeStatus = models.BooleanField(_("Store Status"),default=True)

    def __str__(self) -> str:
        return "{} Ph:{}".format(self.storeName,self.storePhoneNo)
    
    def fullStoreAddress(self):
        addr = self.storeAddress + ", " +self.storeLocality +", " + str(self.storeLocalityPinCode)
        return addr

class StoreProductsDetails(models.Model):
    store = models.ForeignKey("stores.StoreDetail", verbose_name=_("Store Detail"), on_delete=models.CASCADE)
    products = models.ForeignKey(Products, verbose_name=_("store products"), on_delete=models.CASCADE)
    available_stock = models.IntegerField(_("available stock (in Nos.)"),default=0)
    
    def __str__(self) -> str:
        return "StoreName: {} ProductName: {} AvailableStock: {}".format(self.store,self.products,self.available_stock)
    
class PoliciesDetails(models.Model):
    refund_policy = QuillField(null=True,blank=True)
    return_policy = QuillField(null=True,blank=True)
    shipping_and_delivery_policy = QuillField(null=True,blank=True)
    payment_type = QuillField(null=True,blank=True)

    
    class Meta:
        verbose_name = _("PoliciesDetails")
        verbose_name_plural = _("PoliciesDetailss")

    def __str__(self):
        return "Policies Details"

    def get_absolute_url(self):
        return reverse("PoliciesDetails_detail", kwargs={"pk": self.pk})
    
class FAQ(models.Model):

    question = models.TextField(_("FAQ Question"), max_length=500)
    answer = models.TextField(_("FAQ Answer"), max_length=5000)

    

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("FAQ_detail", kwargs={"pk": self.pk})




    

