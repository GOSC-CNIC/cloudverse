# Generated by Django 4.2.9 on 2024-11-27 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_netflow', '0003_remove_menu2chart_title_menu2chart_admin_remark_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartmodel',
            name='is_reverse',
            field=models.BooleanField(default=False, verbose_name='上传流量和下载流量是否反转'),
        ),
    ]