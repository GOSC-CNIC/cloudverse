# Generated by Django 3.2.5 on 2022-05-11 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0002_initial'),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storagequota',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='storage_quotas', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='objectsservice',
            name='data_center',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='object_service_set', to='service.datacenter', verbose_name='数据中心'),
        ),
        migrations.AddField(
            model_name='objectsservice',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='object_service_set', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='bucketarchive',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bucket_archive_set', to='storage.objectsservice', verbose_name='所属服务'),
        ),
        migrations.AddField(
            model_name='bucketarchive',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bucket_archive_set', to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='bucket',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bucket_set', to='storage.objectsservice', verbose_name='所属服务'),
        ),
        migrations.AddField(
            model_name='bucket',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bucket_set', to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
    ]