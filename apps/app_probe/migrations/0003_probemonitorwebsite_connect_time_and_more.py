# Generated by Django 4.2.9 on 2024-04-17 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_probe', '0002_alter_probemonitorwebsite_creation'),
    ]

    operations = [
        migrations.AddField(
            model_name='probemonitorwebsite',
            name='connect_time',
            field=models.FloatField(default=0, verbose_name='TCP 建立持续时间'),
        ),
        migrations.AddField(
            model_name='probemonitorwebsite',
            name='processing_time',
            field=models.FloatField(default=0, verbose_name='连接成功到收到内容时间'),
        ),
        migrations.AddField(
            model_name='probemonitorwebsite',
            name='resolve_time',
            field=models.FloatField(default=0, verbose_name='DNS 解析时间'),
        ),
        migrations.AddField(
            model_name='probemonitorwebsite',
            name='status',
            field=models.FloatField(default=0, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='probemonitorwebsite',
            name='tls_time',
            field=models.FloatField(default=0, verbose_name='tls 时间'),
        ),
        migrations.AddField(
            model_name='probemonitorwebsite',
            name='transfer_time',
            field=models.FloatField(default=0, verbose_name='响应内容时间'),
        ),
    ]