# Generated by Django 4.1.3 on 2023-02-04 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_remove_productreviewandratings_prodreviews_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='longname',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
