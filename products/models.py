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
from django.utils.text import slugify
User = get_user_model()
import os
# from dotenv import load_dotenv
# load_dotenv()

user = get_user_model()

CATEGORIES = (('new-arrival', 'New Arrival'), ('best-seller', 'Best Seller'), ('trending', 'Trend Products'),
              ('Featured Products', 'Featured Products'), ('kids-collection', 'Kids Collection'),('hot-collection','Hot Collection'),('men-collection', 'Men Collection'),('women-collection', 'Women Collection'),('alto-collection','Alto Collection'))
TAGS = (('cotton', 'Cotton'), ('synthetic',
                               'Synthetic'), ('woolen', 'Woolen'), ('polyster', 'Polyster'),('sports','Sports'),('running','Running'))
SIZES = (('XS','XS'),('S','S'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL'),('XXXL','XXXL'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('Double, King','Double, King'),('Double, Queen','Double, Queen'),('Single','Single'),('free-size','Free Size'))
SUBCATEGORIES = (('t-shirt-men','Tshirt Men'),('t-shirt-women','Tshirt Women'),('trouser','Trouser'),('night-wear-men','Night Wear Men'),('night-wear-women','Night Wear Women'),('belts-gents','Belts Men'),('belts-women','Belts Women'),('kurta','Kurta'),('kurti','Kurti'),('format-shirt-men','Formatshirt Men'),('format-shirt-women','Formatshirt Women'),('formal-pants-men','Formal Pants Men'),('formal-pants-women','Formal Pants Women'),('wrist-watches','Wrist Watches'),('shoes-men','Shoes Men'),('shoes-women','Shoes Women'),('sandels-men','Sandels Men'),('sandels-women','Sandels Women'),('beauty-products','Beauty Products'),('tops','Top'),('crop-tops','Crop Tops'),('long-skirts','Long Skirt'),('anarkali-suit','Anarkali Suit'))
COLOR = (('pink','Pink'),('purple','Purple'),('black','Black'),('blue','Blue'),('green','Green'),('red','Red'),('light-white','Light White'),('navy','Navy'),('brown','Brown'),('ash','Ash'),('yellow','Yellow'),('orange','Orange'),('wood','Wood'))


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

class Categories(models.Model):  # ----Category Details----#

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(
        max_length=255, null=False, default=None, unique=True)
    category_code = models.CharField(_("Category Code"), max_length=50,null=True,blank=True) 
    desc = models.TextField(null=True, default=None,
                            blank=True, max_length=1024)
    

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "Categories"
        verbose_name_plural = 'Categories'


class CategorySubCategories(models.Model):

    category = models.ForeignKey(Categories, verbose_name=_(
        "Pro Category"), on_delete=models.CASCADE)
    subcategory = models.CharField(_("SubCategory"), max_length=50)
    subcategory_code = models.CharField(_("Sub Category Code"), max_length=50,null=True,blank=True)

    def __str__(self) -> str:
        return "Category: {} Sub-Category: {}".format(self.category, self.subcategory)
    
    def category_name(self):
        return self.category.category_name

    class Meta:
        db_table = "SubCategories"
        verbose_name_plural = 'SubCategories'

class ProductSize(models.Model):
    subcategory = models.ManyToManyField(CategorySubCategories, verbose_name=_("Sub Category"),blank=True)
    name = models.CharField(_("Name"), max_length=50,null=True, blank=True)
    code = models.CharField(_("Code"), max_length=50, null=True, blank=True)
    size_in_cm = models.CharField(_("Size (in cm)"), max_length=50,null=True, blank=True)
    standard = models.CharField(_("Standard"), max_length=50,null=True,blank=True)
    us_standard = models.CharField(_("US Standard"), max_length=50,null=True,blank=True)
    uk_standard = models.CharField(_("UK Standard"), max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = _("ProductSize")
        verbose_name_plural = _("ProductSizes")

    def __str__(self):
        return "{}".format(self.code)
    
    def subCategoryName(self):
        return ",".join([category.subcategory for category in self.subcategory.all()])

    def get_absolute_url(self):
        return reverse("ProductSize_detail", kwargs={"pk": self.pk})

class ProductTag(models.Model):
    subcategory = models.ManyToManyField(CategorySubCategories, verbose_name=_("Sub Category"),blank=True)
    name = models.CharField(_("Name"), max_length=50,null=True, blank=True)
    code = models.CharField(_("Code"), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _("ProductTag")
        verbose_name_plural = _("ProductTags")

    def __str__(self):
        return self.name
    
    def subCategoryName(self):
        return ",".join([category.subcategory for category in self.subcategory.all()])
    
    def save(self, *args, **kwargs):
        self.code = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ProductTag_detail", kwargs={"pk": self.pk})





class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(_("Slug Field"),unique=True,null=True,blank=True)
    longname = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    desc = QuillField(null=True, blank=True)
    category = models.ManyToManyField(Categories, verbose_name=_("Category"), blank=True)
    
    subcategory = models.ManyToManyField(CategorySubCategories, verbose_name=_("Sub Category"),blank=True)
    image1 = models.BinaryField(_("Product Image 1"), blank=True, null=True,editable=True)
    image2 = models.BinaryField(_("Product Image 2"), blank=True, null=True,editable=True)
    image3 = models.BinaryField(_("Product Image 3"), blank=True, null=True,editable=True)
    unit = models.CharField(max_length=50, blank=True)
    brand = models.CharField(_("Brand"), max_length=50, null=False,default="")
    available_sizes = models.ManyToManyField(ProductSize, verbose_name=_("Sizes"),blank=True)
    tags = models.ManyToManyField(ProductTag, verbose_name=_("Tags"),blank=True)
    vendor = models.ForeignKey(VendorDetail,
                               related_name="Vendor", on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    max_retail_price = models.DecimalField(
        _("MRP (in Rs.)"), max_digits=8, decimal_places=2, null=True)
    discount = models.DecimalField(
        _("Discount (in %)"), max_digits=5, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(
        _("Stock"), default=0)
    average_rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True)
    display_home = models.BooleanField(_("Display at home"), default=True)
    status = models.BooleanField(_("Product Status"), default=True)
    created_at = models.DateTimeField(_("Created Date"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified Date"), auto_now=True)

    def __str__(self):
        return "Name: {} \tUnit: {}\t MRP: {}".format(self.name, self.unit, self.max_retail_price)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        rating = ProductReviewAndRatings.objects.filter(product=self.id).aggregate(
            Avg("ratings")
        )
        self.average_rating = int(
                rating["ratings__avg"] if rating["ratings__avg"] is not None else 0
            )
        super().save(*args, **kwargs)
    
    def sizes(self):
        sizes = [size for size in self.available_sizes.all()]
        return sizes

    def get_attrib_id(self):
        return self.id

    def list_price(self):
        listprice = self.max_retail_price - \
            ((self.discount/100)*self.max_retail_price)
        return round(listprice,2)

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
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
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




class Banners(models.Model):
    ChoiceStatus = (('Activate', 'ACTIVATE'), ('Deactivate', 'DEACTIVATE'),)
    BannerPosition = (("homepage", "HOME PAGE"), ('categoriespage', 'CATEGORIES PAGE'), ('productpage', 'PRODUCT PAGE'), ('top', 'TOP'), ('middle', 'MIDDLE'), ('bottom',
                                                                                                                                                                'BOTTOM'), ('right', 'RIGHT'), ('left', 'LEFT'), ('newarrival', 'NEW ARRIVAL'), ('men', 'MEN'), ('kids', 'KIDS'), ('women', 'WOMEN'), ('cosmetics', 'COSMETICS'), ('browse-more', 'Browse More'))
    position = ModifiedArrayField(models.CharField(
        _("Banner Position"), max_length=255, choices=BannerPosition, null=True, blank=True), blank=True, null=True)
    banner_name = models.CharField(
        _("Banner Name"), max_length=50, null=True, blank=True)
    banner_product_category = models.ManyToManyField(Categories, verbose_name=_("Category"), blank=True)
    banner_desc = QuillField(null=True, blank=True)
    # banner_images = models.ImageField(
        # _("Banner Image"), upload_to="banners/media/images/%Y/%m/%d", height_field=None, width_field=None, max_length=None)
    banner_images = models.BinaryField(_("Banner Image"), blank=True, null=True,editable=True)
    banner_status = models.CharField(
        max_length=20, choices=ChoiceStatus, null=False, default=None)
    products_available = models.IntegerField(
        _("Products Available"), blank=True, null=True)

    def __str__(self):
        return "Banner Name: {}, Banner Status: {}".format(self.banner_name, self.banner_status)

    class Meta:
        db_table = "Banners"
        verbose_name_plural = 'Banners'

    def binaryToStringImage1(self):
        return b64encode(self.banner_images).decode('utf-8')
    
    def scheme_image_tag(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.banner_images).decode('utf8')
        ))

    scheme_image_tag.short_description = 'Image'
    scheme_image_tag.allow_tags = True