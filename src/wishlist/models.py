from django.db import models
from django.conf import settings
from stores.models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from math import ceil

User = get_user_model()


# Create your models here.
class WishlistItems(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'WishlistItems'

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return ceil(self.quantity * self.item.max_retail_price)

    def get_total_discount_item_price(self):
        return ceil(self.quantity * ((self.item.discount/100)*self.item.max_retail_price))

    def get_amount_saved(self):
        return ceil(self.get_total_item_price() - self.get_total_discount_item_price())

    def amount_after_applying_discount(self):
        return ceil(self.get_total_item_price() - self.get_total_discount_item_price())

    def get_final_price(self):
        if self.item.discount:
            return ceil(self.amount_after_applying_discount())
        return ceil(self.get_total_item_price())

    def get_product_name(self):
        return self.item.name


class Wishlist(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(WishlistItems)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Wishlist'

    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return ceil(total)

    def get_max_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return ceil(total)

    def get_order_name(self):
        name = ''
        for order_item in self.items.all():
            name = order_item.get_product_name()
        return name

    def get_total_items_in_order(self):
        return len(self.items.all()) - 1

    def get_quantity(self):
        qty = 0
        for order_item in self.items.all():
            qty += order_item.quantity

        return qty

    def get_total_discount(self):
        return ceil(self.get_max_total() - self.get_total())
