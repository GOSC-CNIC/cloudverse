# Generated by Django 4.2.9 on 2024-06-17 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_global', '0003_ipaccesswhitelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalconfig',
            name='value',
            field=models.TextField(default='', verbose_name='配置内容'),
        ),
    ]
