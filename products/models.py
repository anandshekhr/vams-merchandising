from django.urls import reverse
from django.conf import settings

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.postgres.fields import ArrayField
from django_quill.fields import QuillField
from django.db.models import Avg, Sum
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from base64 import b64encode
from django.utils.text import slugify

from user.models import CustomUser
User = get_user_model()
from math import ceil
import random

# Create your models here.

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

class Categories(models.Model):  # ----Category Details----#

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(
        max_length=255, null=False, default=None, unique=True)
    category_code = models.CharField(_("Category Code"), max_length=50,null=True,blank=True) 
    desc = models.TextField(null=True, default=None,
                            blank=True, max_length=1024)
    
    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        self.category_code = slugify(self.category_name)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "Categories"
        verbose_name_plural = 'Categories'


class CategorySubCategories(models.Model):

    category = models.ForeignKey(Categories, verbose_name=_(
        "Pro Category"), on_delete=models.CASCADE,null=True,blank=True)
    subcategory = models.CharField(_("SubCategory"), max_length=50)
    subcategory_code = models.CharField(_("Sub Category Code"), max_length=50,null=True,blank=True)
    desc = models.TextField(null=True, default=None,
                            blank=True, max_length=1024)

    def __str__(self) -> str:
        return "Category: {} Sub-Category: {}".format(self.category, self.subcategory)
    
    def category_name(self):
        return self.category.category_name
    
    def save(self, *args, **kwargs):
        self.subcategory_code = slugify(self.subcategory)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "SubCategories"
        verbose_name_plural = 'SubCategories'


class CategorySubSubCategories(models.Model):

    subcategory = models.ForeignKey(CategorySubCategories, verbose_name=_(
        "Pro Category"), on_delete=models.CASCADE,null=True,blank=True)
    subsubcategory = models.CharField(_("SubCategory"), max_length=50)
    subsubcategory_code = models.CharField(_("Sub Category Code"), max_length=50,null=True,blank=True)
    desc = models.TextField(null=True, default=None,
                            blank=True, max_length=1024)

    def __str__(self) -> str:
        return "Category: {} Sub-Category: {}".format(self.subcategory, self.subsubcategory)
    
    def category_name(self):
        return self.subcategory.subcategory
    
    def save(self, *args, **kwargs):
        self.subsubcategory_code = slugify(self.subsubcategory)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "SubSubCategories"
        verbose_name_plural = 'SubSubCategories'

class Brand(models.Model):
    name = models.CharField(_("Brand"), max_length=50)
    catergory = models.ForeignKey(Categories, verbose_name=_("category"), on_delete=models.CASCADE)
    image = models.BinaryField(_("brand_logo"), blank=True, null=True,editable=True)
    
    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Brand_detail", kwargs={"pk": self.pk})

class ProductTag(models.Model):
    name = models.CharField(_("Name"), max_length=50,null=True, blank=True)
    code = models.CharField(_("Code"), max_length=50, null=True, blank=True)
    category = models.ManyToManyField(Categories, verbose_name=_("category"))
    sub_category = models.ManyToManyField(CategorySubCategories, verbose_name=_("_subcategory"))
    sub_sub_category = models.ManyToManyField(CategorySubSubCategories, verbose_name=_("sub_sub_category"))

    class Meta:
        verbose_name = _("ProductTag")
        verbose_name_plural = _("ProductTags")

    def __str__(self):
        return self.name
    
    def subCategoryName(self):
        return ",".join([category.category_name for category in self.category.all()])
    
    def save(self, *args, **kwargs):
        self.code = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ProductTag_detail", kwargs={"pk": self.pk})

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


class Banners(models.Model):
    BannerPosition = (("homepage", "HOME PAGE"), ('categoriespage', 'CATEGORIES PAGE'), ('productpage', 'PRODUCT PAGE'), ('top', 'TOP'), ('middle', 'MIDDLE'), ('bottom','BOTTOM'), ('right', 'RIGHT'), ('left', 'LEFT'), ('newarrival', 'NEW ARRIVAL'), ('men', 'MEN'), ('kids', 'KIDS'), ('women', 'WOMEN'), ('cosmetics', 'COSMETICS'), ('browse-more', 'Browse More'))
    position = ModifiedArrayField(models.CharField(
        _("Banner Position"), max_length=255, choices=BannerPosition, null=True, blank=True), blank=True, null=True)
    banner_name = models.CharField(
        _("Banner Name"), max_length=50, null=True, blank=True)
    banner_product_category = models.ForeignKey(Categories, verbose_name=_("Category"), blank=True,on_delete=models.CASCADE,default="")
    banner_images = models.BinaryField(_("Banner Image"), blank=True, null=True,editable=True)
    banner_status = models.BooleanField(_("Banner Status"),default=False)
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

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    sku = models.CharField(_("SKU"), max_length=50,unique=True,default=''.join(random.choice('0123456789') for _ in range(6)))
    
    name = models.CharField(max_length=150)
    longname = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    slug = models.SlugField(_("Slug Field"),unique=True,null=True,blank=True,max_length=250)
    desc = QuillField(null=True, blank=True)

    # Categories related
    category = models.ManyToManyField(Categories, verbose_name=_("Category"), blank=True)
    subcategory = models.ManyToManyField(CategorySubCategories, verbose_name=_("Sub Category"),blank=True)
    subsubcategory = models.ManyToManyField(CategorySubSubCategories, verbose_name=_("Sub Sub Category"),blank=True)
    
    # image thumbnail
    thumbnail = models.BinaryField(_("Thumbnail"), blank=True, null=True,editable=True)
    
    unit = models.CharField(max_length=50, blank=True,choices=(('kgs', 'kgs'),('pc', 'pc'),('cm', 'cm'),('gms', 'gms'),('kgs', 'kgs'),('gb', 'gb'),('ltrs', 'ltrs')))
    brand = models.ForeignKey(Brand, verbose_name=_("Brand"), on_delete=models.CASCADE, blank=True,null=True)
    available_sizes = models.ManyToManyField(ProductSize, verbose_name=_("Sizes"))
    tags = models.ManyToManyField(ProductTag, verbose_name=_("Tags"))
    
    # price related
    max_retail_price = models.DecimalField(_("MRP (in Rs.)"), max_digits=8, decimal_places=2, null=True)
    discount_type = models.CharField(_("Discount Type"), max_length=50,choices=(('percentage', 'percentage'),('flat','flat')),default=('percentage','percentage'))
    discount = models.DecimalField(_("Discount"), max_digits=5, decimal_places=2, null=True, blank=True)
    
    # seller 
    seller = models.ForeignKey(CustomUser,
                               related_name="Vendor", on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    
    # meta related fields
    meta_title = models.CharField(_("Meta Title"), max_length=300)
    meta_description = models.TextField(_("Meta Description"))
    meta_image = models.BinaryField(_("Meta Image"), blank=True, null=True, editable=True)

    display_home = models.BooleanField(_("Display at home"), default=True)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    stock = models.IntegerField(_("Stock"), default=1)
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
    
    # def brand_name(self):
    #     return self.brand.name

    def get_attrib_id(self):
        return self.id

    def selling_price(self):
        """Price at which products are sold

        Returns:
            decimal: price with 2 decimal point
        """
        if self.discount_type == "percentage":
            listprice = self.max_retail_price - \
                ((self.discount/100)*self.max_retail_price)
        
        elif self.discount_type == "flat":
            listprice = self.max_retail_price - self.discount

        return round(listprice,2)
    
    def price_gst_included(self):
        gst_amount = (float(self.selling_price()) * (settings.GST_STICHED/100))
        total = ceil(gst_amount) + self.selling_price()
        return round(total)
    
    def mrp_gst_included(self):
        gst_amount = (float(self.max_retail_price) * (settings.GST_STICHED/100))
        total = ceil(gst_amount) + self.max_retail_price
        return round(total)


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
            images.append(img)
        return images
    
    def scheme_image_tag(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.thumbnail).decode('utf8')
        ))

    scheme_image_tag.short_description = 'Image'
    scheme_image_tag.allow_tags = True

    def binaryToStringThumbnail(self):
        return b64encode(self.thumbnail).decode('utf-8')

    class Meta:
        db_table = "Products"
        verbose_name_plural = 'Products'

class ProductReviewAndRatings(models.Model):
    product = models.ForeignKey(Products, verbose_name=_(
        "product rating"), on_delete=models.CASCADE,null=True,blank=True)
    RATINGS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
    author = models.ForeignKey(User, verbose_name=_(
        "Author Id"), on_delete=models.CASCADE,null=True,blank=True)
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



class ProductImages(models.Model):
    product = models.ForeignKey("Products", related_name="prodImages", on_delete=models.CASCADE, null=False, blank=False, default="")

    image_1 = models.BinaryField(_("Image_1"), blank=True, null=True,editable=True)
    image_2 = models.BinaryField(_("Image_2"), blank=True, null=True,editable=True)
    image_3 = models.BinaryField(_("Image_3"), blank=True, null=True,editable=True)
    image_4 = models.BinaryField(_("Image_4"), blank=True, null=True,editable=True)
    image_5 = models.BinaryField(_("Image_5"), blank=True, null=True,editable=True)
    image_6 = models.BinaryField(_("Image_6"), blank=True, null=True,editable=True)
    image_7 = models.BinaryField(_("Image_7"), blank=True, null=True,editable=True)
    image_8 = models.BinaryField(_("Image_8"), blank=True, null=True,editable=True)


    def __str__(self):
        return "Product: {}".format(self.product)
    
    def binaryToStringimage1(self):
        return b64encode(self.image_1).decode('utf-8')
    
    def scheme_image_tag_image_1(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.image_1).decode('utf8')
        ))

    def binaryToStringimage2(self):
        return b64encode(self.image_2).decode('utf-8')
    
    def scheme_image_tag_image_2(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.image_2).decode('utf8')
        ))
    
    def binaryToStringimage3(self):
        return b64encode(self.image_3).decode('utf-8')
    
    def scheme_image_tag_image_3(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.image_3).decode('utf8')
        ))
    
    def binaryToStringimage4(self):
        return b64encode(self.image_4).decode('utf-8')
    
    def scheme_image_tag_image_4(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.image_4).decode('utf8')
        ))
    
    def binaryToStringimage5(self):
        return b64encode(self.image_5).decode('utf-8')
    
    def scheme_image_tag_image_5(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.image_5).decode('utf8')
        ))
    
    def binaryToStringimage6(self):
        return b64encode(self.image_6).decode('utf-8')
    
    def scheme_image_tag_image_6(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.image_6).decode('utf8')
        ))
    
    def binaryToStringimage7(self):
        return b64encode(self.image_7).decode('utf-8')
    
    def scheme_image_tag_image_7(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.image_7).decode('utf8')
        ))
    
    def binaryToStringimage8(self):
        return b64encode(self.image_8).decode('utf-8')
    
    def scheme_image_tag_image_8(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="100px" height="100px" style="object-fit: scale-down;">'.format(
            b64encode(self.image_8).decode('utf8')
        ))

    class Meta:
        db_table = "ProductImages"
        verbose_name_plural = 'ProductImages'
