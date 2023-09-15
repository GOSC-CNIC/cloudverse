# Generated by Django 4.2.4 on 2023-08-29 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('storage', '0001_initial'),
        ('metering', '0002_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meteringobjectstorage',
            name='service',
            field=models.ForeignKey(db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='storage.objectsservice', verbose_name='服务'),
        ),
        migrations.AddField(
            model_name='meteringdisk',
            name='service',
            field=models.ForeignKey(db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='service.serviceconfig', verbose_name='服务'),
        ),
        migrations.AddField(
            model_name='dailystatementserver',
            name='service',
            field=models.ForeignKey(db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='service.serviceconfig', verbose_name='服务'),
        ),
        migrations.AddField(
            model_name='dailystatementobjectstorage',
            name='service',
            field=models.ForeignKey(db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='storage.objectsservice', verbose_name='对象存储服务单元'),
        ),
        migrations.AddField(
            model_name='dailystatementdisk',
            name='service',
            field=models.ForeignKey(db_constraint=False, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='service.serviceconfig', verbose_name='服务单元'),
        ),
        migrations.AddConstraint(
            model_name='meteringserver',
            constraint=models.UniqueConstraint(fields=('date', 'server_id'), name='unique_date_server'),
        ),
        migrations.AddConstraint(
            model_name='meteringobjectstorage',
            constraint=models.UniqueConstraint(fields=('date', 'storage_bucket_id'), name='unique_date_bucket'),
        ),
        migrations.AddConstraint(
            model_name='meteringdisk',
            constraint=models.UniqueConstraint(fields=('date', 'disk_id'), name='unique_date_disk'),
        ),
    ]