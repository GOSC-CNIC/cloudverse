# Generated by Django 3.1.7 on 2021-03-31 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20210305_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquota',
            name='due_time',
            field=models.DateTimeField(blank=True, default=None, help_text='使用此配额创建的资源的到期时间', null=True, verbose_name='资源使用到期时间'),
        ),
    ]