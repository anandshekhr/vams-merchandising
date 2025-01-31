# Generated by Django 5.0.3 on 2024-06-24 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetaDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('meta_title', models.CharField(blank=True, default='Online Shopping for Women, Men, Kids Fashion & Lifestyle', max_length=500, null=True)),
                ('meta_tag', models.TextField(blank=True, default='', null=True)),
                ('meta_description', models.TextField(blank=True, default='', null=True)),
                ('canonical', models.TextField(blank=True, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.CharField(blank=True, max_length=500, null=True, verbose_name='Notification')),
                ('message', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]
