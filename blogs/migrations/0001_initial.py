# Generated by Django 3.2.5 on 2023-08-24 15:13

from django.db import migrations, models
import django_quill.fields
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=500, verbose_name='Blogs Title')),
                ('content', django_quill.fields.QuillField(blank=True, null=True)),
                ('tags', products.models.ModifiedArrayField(base_field=models.CharField(blank=True, choices=[('LifeStyle', 'Lifestyle'), ('Food', 'Food'), ('Travel', 'Travel')], max_length=50, null=True, verbose_name='Blogs Tags'), null=True, size=None)),
                ('mainpage_image', models.ImageField(blank=True, null=True, upload_to='blogs/media/mainPageImage/%Y/%m/%d', verbose_name='Main Page Image')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='blogs/media/BlogImages/%Y/%m/%d', verbose_name='Blog Image 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='blogs/media/BlogImages/%Y/%m/%d', verbose_name='Blog Image 2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='blogs/media/BlogImages/%Y/%m/%d', verbose_name='Blog Image 3')),
                ('imageMain', models.ImageField(blank=True, null=True, upload_to='blogs/media/BlogBgImages/%Y/%m/%d', verbose_name='Blog Title Background Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name_plural': 'Blogs',
                'db_table': 'Blogs',
                'ordering': ['-created_at'],
            },
        ),
    ]
