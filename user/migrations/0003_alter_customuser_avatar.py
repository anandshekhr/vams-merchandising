# Generated by Django 4.0.4 on 2023-09-01 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user/20230901', verbose_name='Avatar'),
        ),
    ]