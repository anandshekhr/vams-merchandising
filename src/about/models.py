from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from base64 import b64encode

# Create your models here.
class VCReview(models.Model):
    username = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    comment = models.CharField(max_length=500)
    avatar = models.BinaryField(blank=True, null=True,editable=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("VCReview")
        verbose_name_plural = _("VCReviews")

    def __str__(self):
        return "Name: {} Active: {}".format(self.username,self.active)

    def get_absolute_url(self):
        return reverse("VCReview_detail", kwargs={"pk": self.pk})
    
    def scheme_image_tag(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="200" height="100">'.format(
            b64encode(self.avatar).decode('utf8')
        ))

    scheme_image_tag.short_description = 'Image'
    scheme_image_tag.allow_tags = True

    def binaryToStringAvatar(self):
        return b64encode(self.avatar).decode('utf-8')
