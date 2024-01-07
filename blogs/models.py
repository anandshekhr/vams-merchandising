from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField
from products.models import ModifiedArrayField
User = get_user_model()
TAGS = (('LifeStyle', 'Lifestyle'), ('Food',
                                       'Food'), ('Travel', 'Travel'),)
# Create your models here.
class Blogs(models.Model):
    title = models.CharField(_("Blogs Title"), max_length=500,default="",null=False)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE,null=True,blank=True)
    content = QuillField(null=True,blank=True)
    tags = ModifiedArrayField(models.CharField(
        _("Blogs Tags"), max_length=50, choices=TAGS, null=True, blank=True), null=True)
    mainpage_image = models.ImageField(
        _("Main Page Image"), upload_to="blogs/media/mainPageImage/%Y/%m/%d",
        null=True, blank=True)
    image1 = models.ImageField(_("Blog Image 1"), upload_to="blogs/media/BlogImages/%Y/%m/%d",
                               null=True, blank=True)
    image2 = models.ImageField(_("Blog Image 2"), upload_to="blogs/media/BlogImages/%Y/%m/%d",
                               null=True, blank=True)
    image3 = models.ImageField(_("Blog Image 3"), upload_to="blogs/media/BlogImages/%Y/%m/%d",
                               null=True, blank=True)
    imageMain = models.ImageField(_("Blog Title Background Image"), upload_to="blogs/media/BlogBgImages/%Y/%m/%d",
                               null=True,blank=True)
    created_at = models.DateTimeField(_("Created Date"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified Date"), auto_now=True)

  
    def __str__(self):
        return self.title

    def tag_string(self):
        cat = ','.join(i for i in self.tags)
        return cat

    class Meta:
        ordering = ['-created_at']
        db_table = "Blogs"
        verbose_name_plural = 'Blogs'
    

