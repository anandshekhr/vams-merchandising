# Generated by Django 4.1.3 on 2023-02-22 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_banners_banner_images_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='average_rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
