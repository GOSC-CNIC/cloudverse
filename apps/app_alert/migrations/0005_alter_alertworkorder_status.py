# Generated by Django 4.2.9 on 2024-04-29 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_alert', '0004_alter_alertworkorder_creation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertworkorder',
            name='status',
            field=models.CharField(choices=[('无需处理', '无需处理'), ('已完成', '已完成'), ('误报', '误报')], default='无需处理', max_length=10, verbose_name='状态'),
        ),
    ]