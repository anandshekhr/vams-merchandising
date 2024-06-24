# Generated by Django 5.0.3 on 2024-06-24 04:11

import django.db.models.deletion
import django_quill.fields
import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(default=None, max_length=255, unique=True)),
                ('category_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Category Code')),
                ('desc', models.TextField(blank=True, default=None, max_length=1024, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.BinaryField(blank=True, editable=True, null=True, verbose_name='Image_1')),
            ],
            options={
                'verbose_name_plural': 'ProductImages',
                'db_table': 'ProductImages',
            },
        ),
        migrations.CreateModel(
            name='ProductReviewAndRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Product Review')),
                ('ratings', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='Product Rating')),
                ('review_date', models.DateTimeField(auto_now=True, verbose_name='review_date')),
                ('is_approved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'ProductReviewAndRatings',
                'db_table': 'ProductReviewAndRatings',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sku', models.CharField(default='504827', max_length=50, unique=True, verbose_name='SKU')),
                ('name', models.CharField(max_length=150)),
                ('longname', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True, verbose_name='Slug Field')),
                ('desc', django_quill.fields.QuillField(blank=True, null=True)),
                ('thumbnail', models.BinaryField(blank=True, editable=True, null=True, verbose_name='Thumbnail')),
                ('unit', models.CharField(blank=True, choices=[('kgs', 'kgs'), ('pc', 'pc'), ('cm', 'cm'), ('gms', 'gms'), ('kgs', 'kgs'), ('gb', 'gb'), ('ltrs', 'ltrs')], max_length=50)),
                ('max_retail_price', models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='MRP (in Rs.)')),
                ('discount_type', models.CharField(choices=[('percentage', 'percentage'), ('flat', 'flat')], default=('percentage', 'percentage'), max_length=50, verbose_name='Discount Type')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Discount')),
                ('meta_title', models.CharField(max_length=300, verbose_name='Meta Title')),
                ('meta_description', models.TextField(verbose_name='Meta Description')),
                ('meta_image', models.BinaryField(blank=True, editable=True, null=True, verbose_name='Meta Image')),
                ('display_home', models.BooleanField(default=True, verbose_name='Display at home')),
                ('average_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('stock', models.IntegerField(default=1, verbose_name='Stock')),
                ('status', models.BooleanField(default=True, verbose_name='Product Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'db_table': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Code')),
                ('size_in_cm', models.CharField(blank=True, max_length=50, null=True, verbose_name='Size (in cm)')),
                ('standard', models.CharField(blank=True, max_length=50, null=True, verbose_name='Standard')),
                ('us_standard', models.CharField(blank=True, max_length=50, null=True, verbose_name='US Standard')),
                ('uk_standard', models.CharField(blank=True, max_length=50, null=True, verbose_name='UK Standard')),
            ],
            options={
                'verbose_name': 'ProductSize',
                'verbose_name_plural': 'ProductSizes',
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'ProductTag',
                'verbose_name_plural': 'ProductTags',
            },
        ),
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', products.models.ModifiedArrayField(base_field=models.CharField(blank=True, choices=[('homepage', 'HOME PAGE'), ('categoriespage', 'CATEGORIES PAGE'), ('productpage', 'PRODUCT PAGE'), ('top', 'TOP'), ('middle', 'MIDDLE'), ('bottom', 'BOTTOM'), ('right', 'RIGHT'), ('left', 'LEFT'), ('newarrival', 'NEW ARRIVAL'), ('men', 'MEN'), ('kids', 'KIDS'), ('women', 'WOMEN'), ('cosmetics', 'COSMETICS'), ('browse-more', 'Browse More')], max_length=255, null=True, verbose_name='Banner Position'), blank=True, null=True, size=None)),
                ('banner_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Banner Name')),
                ('banner_images', models.BinaryField(blank=True, editable=True, null=True, verbose_name='Banner Image')),
                ('banner_status', models.BooleanField(default=False, verbose_name='Banner Status')),
                ('products_available', models.IntegerField(blank=True, null=True, verbose_name='Products Available')),
                ('banner_product_category', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='products.categories', verbose_name='Category')),
            ],
            options={
                'verbose_name_plural': 'Banners',
                'db_table': 'Banners',
            },
        ),
        migrations.CreateModel(
            name='CategorySubCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(max_length=50, verbose_name='SubCategory')),
                ('subcategory_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Sub Category Code')),
                ('desc', models.TextField(blank=True, default=None, max_length=1024, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.categories', verbose_name='Pro Category')),
            ],
            options={
                'verbose_name_plural': 'SubCategories',
                'db_table': 'SubCategories',
            },
        ),
        migrations.CreateModel(
            name='CategorySubSubCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subsubcategory', models.CharField(max_length=50, verbose_name='SubCategory')),
                ('subsubcategory_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Sub Category Code')),
                ('desc', models.TextField(blank=True, default=None, max_length=1024, null=True)),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.categorysubcategories', verbose_name='Pro Category')),
            ],
            options={
                'verbose_name_plural': 'SubSubCategories',
                'db_table': 'SubSubCategories',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Brand')),
                ('image', models.BinaryField(blank=True, editable=True, null=True, verbose_name='brand_logo')),
                ('catergory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.categories', verbose_name='category_id')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.categorysubcategories', verbose_name='subcategory_id')),
                ('subsubcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.categorysubsubcategories', verbose_name='subsubcategory_id')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
    ]
