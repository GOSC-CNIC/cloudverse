# Generated by Django 4.2.9 on 2024-11-05 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0008_evcloudpermslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='disk',
            name='created_user',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='server',
            name='created_user',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='serverarchive',
            name='created_user',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='创建人'),
        ),
    ]
