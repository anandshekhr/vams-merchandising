# Generated by Django 4.1.3 on 2023-02-20 07:08

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_banners_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='position',
            field=products.models.ModifiedArrayField(base_field=models.CharField(blank=True, choices=[('Home Page', 'HOME PAGE'), ('Categories Page', 'CATEGORIES PAGE'), ('Product Page', 'PRODUCT PAGE'), ('Top', 'TOP'), ('Middle', 'MIDDLE'), ('Bottom', 'BOTTOM'), ('Right', 'RIGHT'), ('Left', 'LEFT')], max_length=255, null=True, verbose_name='Banner Position'), blank=True, null=True, size=None),
        ),
    ]
