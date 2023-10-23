from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
# Create your models here.
class PaymentsEmails(models.Model):
    MAIN_SUBCATEGORY = (
        ('Retry', 'Retry'),
        ('Failed', 'Failed'),
        ('Successfull', 'Successfull'),
        ('Complaint', 'Complaint'),
    )
    category =  models.CharField(max_length=200, default='', choices=MAIN_SUBCATEGORY,null=True,blank=True)
    email_name =  models.CharField(max_length=200, default='',null=True,blank=True)
    subject =  models.CharField(max_length=200, default='',null=True,blank=True)
    body =  models.TextField(default='',null=True,blank=True)
    sms_body =  models.TextField(default='',null=True,blank=True)
    sender = models.CharField(max_length=200, default='',null=True,blank=True)
    templateid = models.CharField(max_length=200, default='',null=True,blank=True)
    is_active =  models.BooleanField(default=True, blank=False)
    create_date =  models.DateTimeField(default=datetime.now(),null=True,blank=True)
    
    def __str__(self):
        return f"{self.category}:{self.email_name}:{self.subject}"
    
    class Meta:
        verbose_name = _("PaymentsEmail")
        verbose_name_plural = _("PaymentsEmails")


class UserRegisteredEmails(models.Model):
    MAIN_SUBCATEGORY = (
        ('New Registration', 'New Registration'),
        ('New Registration to admin', 'New Registration to admin'),
    )
    category =  models.CharField(max_length=200, default='', choices=MAIN_SUBCATEGORY,null=True,blank=True)
    email_name =  models.CharField(max_length=200, default='',null=True,blank=True)
    subject =  models.CharField(max_length=200, default='',null=True,blank=True)
    body =  models.TextField(default='',null=True,blank=True)
    sms_body =  models.TextField(default='',null=True,blank=True)
    sender = models.CharField(max_length=200, default='',null=True,blank=True)
    templateid = models.CharField(max_length=200, default='',null=True,blank=True)
    DltPrincipalEntityId = models.CharField(max_length=200, default='',null=True,blank=True)
    is_active =  models.BooleanField(default=True, blank=False)
    create_date =  models.DateTimeField(default=datetime.now(),null=True,blank=True)
    
    def __str__(self):
        return f"{self.category}:{self.email_name}:{self.subject}"
    
    class Meta:
        verbose_name = _("UserRegisteredEmail")
        verbose_name_plural = _("UserRegisteredEmails")
    
class PromotionalEmails(models.Model):
    MAIN_SUBCATEGORY = (
        ('Reccuring', 'Reccuring'),
        ('Promotional Offer', 'Promotional Offer'),
    )
    category =  models.CharField(max_length=200, default='', choices=MAIN_SUBCATEGORY,null=True,blank=True)
    email_name =  models.CharField(max_length=200, default='',null=True,blank=True)
    subject =  models.CharField(max_length=200, default='',null=True,blank=True)
    body =  models.TextField(default='',null=True,blank=True)
    sms_body =  models.TextField(default='',null=True,blank=True)
    sender = models.CharField(max_length=200, default='',null=True,blank=True)
    templateid = models.CharField(max_length=200, default='',null=True,blank=True)
    DltPrincipalEntityId = models.CharField(max_length=200, default='',null=True,blank=True)
    is_active =  models.BooleanField(default=True, blank=False)
    create_date =  models.DateTimeField(default=datetime.now(),null=True,blank=True)
    
    def __str__(self):
        return f"{self.category}:{self.email_name}:{self.subject}"
    
    class Meta:
        verbose_name = _("PromotionalEmail")
        verbose_name_plural = _("PromotionalEmails")
    
class DelayDeliveryAndRefundEmails(models.Model):
    MAIN_SUBCATEGORY = (
        ('Delivery Delay','Delivery Delay'),
        ('Refund Requested','Refund Requested'),
        ('Refund Processed','Refund Processed'),
        ('Refunded','Refunded'),
    )
    category =  models.CharField(max_length=200, default='', choices=MAIN_SUBCATEGORY,null=True,blank=True)
    email_name =  models.CharField(max_length=200, default='',null=True,blank=True)
    subject =  models.CharField(max_length=200, default='',null=True,blank=True)
    body =  models.TextField(default='',null=True,blank=True)
    sms_body =  models.TextField(default='',null=True,blank=True)
    sender = models.CharField(max_length=200, default='',null=True,blank=True)
    templateid = models.CharField(max_length=200, default='',null=True,blank=True)
    DltPrincipalEntityId = models.CharField(max_length=200, default='',null=True,blank=True)
    is_active =  models.BooleanField(default=True, blank=False)
    create_date =  models.DateTimeField(default=datetime.now(),null=True,blank=True)
    
    def __str__(self):
        return f"{self.category}:{self.email_name}:{self.subject}"

    class Meta:
        verbose_name = _("DelayDeliveryAndRefundEmail")
        verbose_name_plural = _("DelayDeliveryAndRefundEmails")

