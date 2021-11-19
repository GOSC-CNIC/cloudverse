# Generated by Django 3.2.5 on 2021-11-19 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20211103_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyvmservice',
            name='cloud_type',
            field=models.CharField(choices=[('public', '公有云'), ('private', '私有云'), ('hybrid ', '混合云')], default='private', max_length=32, verbose_name='云服务类型'),
        ),
        migrations.AddField(
            model_name='serviceconfig',
            name='cloud_type',
            field=models.CharField(choices=[('public', '公有云'), ('private', '私有云'), ('hybrid ', '混合云')], default='private', max_length=32, verbose_name='云服务类型'),
        ),
        migrations.AlterField(
            model_name='applyvmservice',
            name='service_type',
            field=models.CharField(choices=[('evcloud', 'EVCloud'), ('openstack', 'OpenStack'), ('vmware', 'VMware'), ('unis-cloud', '紫光云')], default='evcloud', max_length=32, verbose_name='服务平台类型'),
        ),
    ]
