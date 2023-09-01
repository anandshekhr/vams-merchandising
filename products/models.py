from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from .storage import ProductFileStorage
from django.contrib.auth import get_user_model
from datetime import date
from django import forms
from django.contrib.postgres.fields import ArrayField
from django_quill.fields import QuillField
from django.db.models import Avg, Sum
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from base64 import b64encode
User = get_user_model()
import os
# from dotenv import load_dotenv
# load_dotenv()

user = get_user_model()

CATEGORIES = (('new-arrival', 'New Arrival'), ('best-seller', 'Best Seller'), ('trending', 'Trend Products'),
              ('Featured Products', 'Featured Products'), ('kids-collection', 'Kids Collection'),('hot-collection','Hot Collection'))
TAGS = (('cotton', 'Cotton'), ('synthetic',
                               'Synthetic'), ('woolen', 'Woolen'), ('polyster', 'Polyster'),)
SIZES = (('XS','XS'),('S','S'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL'),('XXL','XXL'))
SUBCATEGORIES = (('t-shirt-men','Tshirt Men'),('t-shirt-women','Tshirt Women'),('trouser','Trouser'),('night-wear-men','Night Wear Men'),('night-wear-women','Night Wear Women'),('belts-gents','Belts Men'),('belts-women','Belts Women'),('kurta','Kurta'),('kurti','Kurti'),('format-shirt-men','Formatshirt Men'),('format-shirt-women','Formatshirt Women'),('formal-pants-men','Formal Pants Men'),('formal-pants-women','Formal Pants Women'),('wrist-watches','Wrist Watches'),('shoes-men','Shoes Men'),('shoes-women','Shoes Women'),('sandels-men','Sandels Men'),('sandels-women','Sandels Women'),('beauty-products','Beauty Products'),('tops','Top'),('crop-tops','Crop Tops'),('long-skirts','Long Skirt'),('anarkali-suit','Anarkali Suit'))


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# MultiArrayChoiceFields



class ModifiedArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": forms.CheckboxSelectMultiple,
            **kwargs
        }
        return super(ArrayField, self).formfield(**defaults)

# Create your models here.


class VendorDetail(models.Model):
    owner = models.ForeignKey(User, verbose_name=_(
        "Owner"), on_delete=models.CASCADE)
    storeName = models.CharField(
        _("Store Name"), max_length=100, null=True, blank=True)
    email = models.EmailField(
        _("Store Email ID"), max_length=254, null=True, blank=True)
    phone_number = models.CharField(
        _("Store Phone No."), max_length=100, null=True, blank=True)
    address = models.TextField(
        _("Store Address"), max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = _("VendorDetail")
        verbose_name_plural = _("VendorDetails")

    def __str__(self):
        return "Owner:{} Store: {}".format(self.owner,self.storeName)

    def get_absolute_url(self):
        return reverse("VendorDetail_detail", kwargs={"pk": self.pk})

class VendorBankAccountDetail(models.Model):
    vendor = models.ForeignKey(VendorDetail, verbose_name=_("Vendor"), on_delete=models.CASCADE)
    bank_name = models.CharField(_("Bank Name"), max_length=50)
    bank_account_number = models.CharField(_("Account No."), max_length=50)
    confirm_bank_account_number = models.CharField(_("Confirm Account No."), max_length=50)
    ifsc_code = models.CharField(_("IFSC Code"), max_length=50)
    upi_id = models.CharField(_("UPI Id"), max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = _("VendorBankAccountDetail")
        verbose_name_plural = _("VendorBankAccountDetails")

    def __str__(self):
        return "Owner: {} Acc. No.{}".format(self.vendor,self.confirm_bank_account_number)

    def get_absolute_url(self):
        return reverse("VendorBankAccountDetail_detail", kwargs={"pk": self.pk})


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    longname = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    desc = QuillField(null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    category = ModifiedArrayField(models.CharField(
        _("Product Category"), max_length=255, choices=CATEGORIES, null=True, blank=True), null=True)
    subcategory = models.CharField(_("Product Sub-Category"), max_length=50, choices=SUBCATEGORIES,null=True,blank=True)
    max_retail_price = models.DecimalField(
        _("MRP (in Rs.)"), max_digits=8, decimal_places=2, null=True)
    # image1 = models.ImageField(_("Product Image 1"), upload_to="product/media/mainImage/%Y/%m/%d",
    #                           height_field=None, width_field=None, max_length=None, null=True, default=None, blank=True)
    image1 = models.BinaryField(_("Product Image 1"), blank=True, null=True,editable=True)
    image2 = models.BinaryField(_("Product Image 2"), blank=True, null=True,editable=True)
    image3 = models.BinaryField(_("Product Image 3"), blank=True, null=True,editable=True)
    brand = models.CharField(_("Brand"), max_length=50, null=True, blank=True)
    available_sizes = ModifiedArrayField(models.CharField(
        _("Product Available"), max_length=255, choices=SIZES, null=True, blank=True), null=True)
    vendor = models.ForeignKey(VendorDetail,
                               related_name="Vendor", on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    tags = ModifiedArrayField(models.CharField(
        _("Tags"), max_length=50, choices=TAGS, null=True, blank=True), null=True)
    discount = models.DecimalField(
        _("Discount (in %)"), max_digits=5, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(
        _("available stock (in Nos.)"), default=0)
    display_home = models.BooleanField(_("Display at home"), default=False)
    new_arrival = models.BooleanField(_("New"), default=False)
    average_rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True)
    status = models.BooleanField(_("Product Status"), default=True)
    created_at = models.DateTimeField(_("Created Date"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified Date"), auto_now=True)

    def __str__(self):
        return "Name: {} \tUnit: {}\t MRP: {}".format(self.name, self.unit, self.max_retail_price)

    def get_attrib_id(self):
        return self.id

    def list_price(self):
        listprice = self.max_retail_price - \
            ((self.discount/100)*self.max_retail_price)
        return listprice

    def cat_string(self):
        cat = ','.join(i for i in self.category)
        return cat

    def tags_string(self):
        tag = ','.join(i for i in self.tags)
        return tag

    @property
    def sold(self):
        return self.cart_set.aggregate(Sum('quantity'))['quantity__sum'] or 0

    @property
    def left(self):
        return self.stock - self.sold

    def pr_images(self):
        images = []
        for img in self.more_images.all():
            print(img)
            images.append(img)
        return images
    
    def scheme_image_tag(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="200" height="100">'.format(
            b64encode(self.image1).decode('utf8')
        ))

    scheme_image_tag.short_description = 'Image'
    scheme_image_tag.allow_tags = True

    def binaryToStringImage1(self):
        return b64encode(self.image1).decode('utf-8')
    
    def binaryToStringImage2(self):
        return b64encode(self.image2).decode('utf-8')
    
    def binaryToStringImage3(self):
        return b64encode(self.image3).decode('utf-8')

    class Meta:
        db_table = "Products"
        verbose_name_plural = 'Products'


class ProductImages(models.Model):
    product = models.ForeignKey(
        "products", related_name="prodImages", on_delete=models.CASCADE, null=False, blank=False, default="")

    images = models.ImageField(_("Product_Image"), upload_to="product/media/photos/%Y/%m/%d",
                               height_field=None, width_field=None, max_length=None)

    image_thumbnail = models.ImageField(
        _("Product Image Thumbnail"), upload_to="product/media/photos/%Y/%m/%d/thumbnails", height_field=None, width_field=None, max_length=None, blank=True, null=True)

    image_thumbnail_color = models.CharField(
        _("Product Thumbnail Color"), max_length=50, null=True, blank=True)

    def __str__(self):
        return "Image URL: {}".format(self.images)

    class Meta:
        db_table = "ProductImages"
        verbose_name_plural = 'ProductImages'


class ProductReviewAndRatings(models.Model):
    product = models.ForeignKey(Products, verbose_name=_(
        "product rating"), on_delete=models.CASCADE)
    RATINGS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
    author = models.ForeignKey(user, verbose_name=_(
        "Author Id"), on_delete=models.CASCADE)
    review = models.CharField(_("Product Review"), max_length=1024, null=True,blank=True)
    ratings = models.IntegerField(
        _("Product Rating"), choices=RATINGS, null=True,blank=True)
    review_date = models.DateTimeField(
        verbose_name="review_date",auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "Author ID: {}, Ratings: {}".format(self.author, self.ratings)

    def get_review_rating(self):
        return self.ratings

    class Meta:
        db_table = "ProductReviewAndRatings"
        verbose_name_plural = 'ProductReviewAndRatings'


class Categories(models.Model):  # ----Catagory Details----#

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(
        max_length=255, null=False, default=None, unique=True)
    desc = models.TextField(null=True, default=None,
                            blank=True, max_length=1024)
    category_image = models.ImageField(_("category image"), upload_to="category/media/photos/%Y/%m/%d",
                                       height_field=None, width_field=None, max_length=None, null=True, blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "Categories"
        verbose_name_plural = 'Categories'


class CategoriesProducts(models.Model):
    categoriesproduct_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, verbose_name=_(
        "Pro Category"), on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name=_(
        "Category Products"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "ID: {} Category: {} Products: {}".format(self.categoriesproduct_id, self.category, self.product)

    class Meta:
        db_table = "CategoriesProducts"
        verbose_name_plural = 'CategoriesProducts'


class Banners(models.Model):
    ChoiceStatus = (('Activate', 'ACTIVATE'), ('Deactivate', 'DEACTIVATE'),)
    BannerPosition = (("homepage", "HOME PAGE"), ('categoriespage', 'CATEGORIES PAGE'), ('productpage', 'PRODUCT PAGE'), ('top', 'TOP'), ('middle', 'MIDDLE'), ('bottom',
                                                                                                                                                                'BOTTOM'), ('right', 'RIGHT'), ('left', 'LEFT'), ('newarrival', 'NEW ARRIVAL'), ('men', 'MEN'), ('kids', 'KIDS'), ('women', 'WOMEN'), ('cosmetics', 'COSMETICS'), ('browse-more', 'Browse More'))
    position = ModifiedArrayField(models.CharField(
        _("Banner Position"), max_length=255, choices=BannerPosition, null=True, blank=True), blank=True, null=True)
    banner_name = models.CharField(
        _("Banner Name"), max_length=50, null=True, blank=True)
    banner_desc = QuillField(null=True, blank=True)
    banner_images = models.ImageField(
        _("Banner Image"), upload_to="banners/media/images/%Y/%m/%d", height_field=None, width_field=None, max_length=None)
    banner_status = models.CharField(
        max_length=20, choices=ChoiceStatus, null=False, default=None)
    products_available = models.IntegerField(
        _("Products Available"), blank=True, null=True)

    def __str__(self):
        return "Banner Name: {}, Banner Status: {}".format(self.banner_name, self.banner_status)

    class Meta:
        db_table = "Banners"
        verbose_name_plural = 'Banners'
