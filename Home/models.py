from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications',null=True,blank=True)
    notification = models.CharField(_("Notification"), max_length=500,null=True,blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.notification

class MetaDetail(models.Model):
    page = models.CharField(default = "" ,max_length = 200, blank = True, null = True)
    meta_title = models.CharField(max_length = 500, default ="", null = True, blank = True)
    meta_tag = models.TextField(default = "", null = True, blank = True)
    meta_description = models.TextField(default = "" , null = True, blank = True)
    canonical = models.TextField(default = "" , null = True, blank = True)
    def __str__(self) :
        return self.meta_title