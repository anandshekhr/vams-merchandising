# Generated by Django 3.2.5 on 2023-08-24 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendordetail',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='products',
            name='vendor',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Vendor', to='products.vendordetail'),
        ),
        migrations.AddField(
            model_name='productreviewandratings',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author Id'),
        ),
        migrations.AddField(
            model_name='productreviewandratings',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='product rating'),
        ),
        migrations.AddField(
            model_name='productimages',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='prodImages', to='products.products'),
        ),
        migrations.AddField(
            model_name='categoriesproducts',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.categories', verbose_name='Pro Category'),
        ),
        migrations.AddField(
            model_name='categoriesproducts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='Category Products'),
        ),
    ]