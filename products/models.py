from django.db import models
from django.utils.translation import gettext_lazy as _
from .storage import ProductFileStorage
from django.contrib.auth import get_user_model
from datetime import date
from django import forms
from django.contrib.postgres.fields import ArrayField
from django_quill.fields import QuillField
from django.db.models import Avg, Sum
import os
from dotenv import load_dotenv
load_dotenv()

user = get_user_model()

CATEGORIES = (('Deal of the day', 'Deal of the day'), ('Best Products', 'Best Products'), ('Trend Products', 'Trend Products'), ('Featured Products', 'Featured Products'), ('Biscuits & Snacks', 'Biscuits & Snacks'), ('Bread & Bakery', 'Bread & Bakery'), ('Breakfast & Dairy', 'Breakfast & Dairy'), ('Frozen Foods', 'Frozen Foods'), ('Fruits & Vegetables',
                                                                                                                                                                                                                                                                                                                                             'Fruits & Vegetables'), ('Grocery & Staples', 'Grocery & Staples'), ('Household Needs', 'Household Needs'), ('Meats & Seafood', 'Meats & Seafood'), ('Eggs Substitutes', 'Eggs Substitutes'), ('Honey Vegetables', 'Honey Vegetables'), ('Marmalades Staples', 'Marmalades Staples'), ('Sour Cream and Dips', 'Sour Cream and Dips'), ('Yogurt Seafood', 'Yogurt Seafood'),)
TAGS = (('Vegetarian', 'Vegetarian'), ('Non-Vegetarian',
                                       'Non-Vegetarian'), ('Organic', 'Organic'),)


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


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    longname = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    desc = QuillField(null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    category = ModifiedArrayField(models.CharField(
        _("Product Category"), max_length=255, choices=CATEGORIES, null=True, blank=True), null=True)
    max_retail_price = models.DecimalField(
        _("MRP (in Rs.)"), max_digits=8, decimal_places=2, null=True)
    image = models.ImageField(_("Product Main Image"), upload_to="product/media/mainImage/%Y/%m/%d",
                              height_field=None, width_field=None, max_length=None, null=True, default=None, blank=True)
    brand = models.CharField(_("Brand"), max_length=50, null=True, blank=True)
    vendor = models.CharField(
        _("Vendor"), max_length=50, null=True, blank=True)
    tags = ModifiedArrayField(models.CharField(
        _("Tags"), max_length=50, choices=TAGS, null=True, blank=True), null=True)
    discount = models.DecimalField(
        _("Discount (in %)"), max_digits=5, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(
        _("available stock (in Nos.)"), default=0)
    display_home = models.BooleanField(_("Display at home"), default=False)
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

    class Meta:
        db_table = "Products"
        verbose_name_plural = 'Products'


class ProductReviewAndRatings(models.Model):
    product = models.ForeignKey("products", verbose_name=_(
        "product rating"), on_delete=models.CASCADE, null=False, blank=False, default="")
    RATINGS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
    author = models.ForeignKey(user, verbose_name=_(
        "Author Id"), on_delete=models.CASCADE)
    review = models.CharField(_("Product Review"), max_length=1024, null=True)
    ratings = models.IntegerField(
        _("Product Rating"), choices=RATINGS, null=True)
    upload_image = models.ImageField(_("ImagesForReview"), upload_to="product/media/reviews/%Y/%m/%d",
                                     height_field=None, width_field=None, max_length=None, null=True)
    review_date = models.DateTimeField(
        verbose_name="review_date", auto_now=True)

    def __str__(self):
        return "Author ID: {}, Ratings: {}".format(self.author, self.ratings)

    def get_review_rating(self):
        return self.ratings

    class Meta:
        db_table = "ProductReviewAndRatings"
        verbose_name_plural = 'ProductReviewAndRatings'


class ProductImages(models.Model):
    product = models.ForeignKey(
        "products", related_name="prodImages", on_delete=models.CASCADE, null=False, blank=False, default="")
    images = models.ImageField(_("Product_Image"), upload_to="product/media/photos/%Y/%m/%d",
                               height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return "Image URL: {}".format(self.images)

    class Meta:
        db_table = "ProductImages"
        verbose_name_plural = 'ProductImages'


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
