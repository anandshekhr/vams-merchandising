# Generated by Django 4.0.4 on 2023-08-29 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_image1_alter_products_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='banner_images',
            field=models.BinaryField(blank=True, editable=True, null=True, verbose_name='Banner Image'),
        ),
    ]