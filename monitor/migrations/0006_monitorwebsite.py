# Generated by Django 3.2.13 on 2023-01-13 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitor', '0005_auto_20221220_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorWebsiteTask',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='', max_length=2048, verbose_name='要监控的网址')),
                ('url_hash', models.CharField(default='', max_length=64, unique=True, verbose_name='网址hash值')),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '网站监控任务',
                'verbose_name_plural': '网站监控任务',
                'db_table': 'monitor_website_task',
                'ordering': ['-creation'],
            },
        ),
        migrations.CreateModel(
            name='MonitorWebsiteVersion',
            fields=[
                ('id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('version', models.BigIntegerField(default=1, help_text='用于区分网站监控任务表是否有变化', verbose_name='监控任务版本号')),
                ('creation', models.DateTimeField(verbose_name='创建时间')),
                ('modification', models.DateTimeField(verbose_name='修改时间')),
                ('provider', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='monitor.monitorprovider', verbose_name='监控查询服务配置信息')),
            ],
            options={
                'verbose_name': '网站监控任务版本',
                'verbose_name_plural': '网站监控任务版本',
                'db_table': 'monitor_website_version_provider',
                'ordering': ['-creation'],
            },
        ),
        migrations.CreateModel(
            name='MonitorWebsite',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, verbose_name='网站名称')),
                ('url', models.URLField(default='', help_text='http(s)://xxx.xxx', max_length=2048, verbose_name='要监控的网址')),
                ('url_hash', models.CharField(default='', max_length=64, verbose_name='网址hash值')),
                ('creation', models.DateTimeField(verbose_name='创建时间')),
                ('modification', models.DateTimeField(verbose_name='修改时间')),
                ('remark', models.CharField(blank=True, default='', max_length=255, verbose_name='备注')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '网站监控',
                'verbose_name_plural': '网站监控',
                'db_table': 'monitor_website',
                'ordering': ['-creation'],
            },
        ),
    ]
