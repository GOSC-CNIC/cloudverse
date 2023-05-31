# Generated by Django 3.2.13 on 2023-05-30 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_auto_20230522_0631'),
        ('order', '0005_auto_20230509_0645'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.PositiveSmallIntegerField(verbose_name='月数')),
                ('enable', models.BooleanField(default=True, verbose_name='可用状态')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('service', models.ForeignKey(blank=True, db_constraint=False, db_index=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='service.serviceconfig', verbose_name='服务单元')),
            ],
            options={
                'verbose_name': '订购时长',
                'verbose_name_plural': '订购时长',
                'db_table': 'order_period',
                'ordering': ['period'],
            },
        ),
    ]