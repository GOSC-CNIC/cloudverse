# Generated by Django 3.2.13 on 2023-05-22 06:31
import math

from django.db import migrations


def pri_quota_ram_mb_to_gb(apps, schema_editor):
    model_cls = apps.get_model("service", "ServicePrivateQuota")
    quotas = model_cls.objects.all()
    for quota in quotas:
        quota.ram_total = math.ceil(quota.ram_total / 1024)
        quota.ram_used = math.ceil(quota.ram_used / 1024)
        quota.save(update_fields=['ram_total', 'ram_used'])

    print('Changed private quota ram unit from MiB to GiB OK', len(quotas))


def pri_quota_ram_gb_to_mb(apps, schema_editor):
    model_cls = apps.get_model("service", "ServicePrivateQuota")
    quotas = model_cls.objects.all()
    for quota in quotas:
        quota.ram_total = quota.ram_total * 1024
        quota.ram_used = quota.ram_used * 1024
        quota.save(update_fields=['ram_total', 'ram_used'])

    print('Changed back private quota ram unit from GiB to Mib OK', len(quotas))


def share_quota_ram_mb_to_gb(apps, schema_editor):
    model_cls = apps.get_model("service", "ServiceShareQuota")
    quotas = model_cls.objects.all()
    for quota in quotas:
        quota.ram_total = math.ceil(quota.ram_total / 1024)
        quota.ram_used = math.ceil(quota.ram_used / 1024)
        quota.save(update_fields=['ram_total', 'ram_used'])

    print('Changed share quota ram unit from MiB to GiB OK', len(quotas))


def share_quota_ram_gb_to_mb(apps, schema_editor):
    model_cls = apps.get_model("service", "ServiceShareQuota")
    quotas = model_cls.objects.all()
    for quota in quotas:
        quota.ram_total = quota.ram_total * 1024
        quota.ram_used = quota.ram_used * 1024
        quota.save(update_fields=['ram_total', 'ram_used'])

    print('Changed back share quota ram unit from GiB to Mib OK', len(quotas))


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20230410_0308'),
    ]

    operations = [
        migrations.RunPython(pri_quota_ram_mb_to_gb, reverse_code=pri_quota_ram_gb_to_mb),
        migrations.RunPython(share_quota_ram_mb_to_gb, reverse_code=share_quota_ram_gb_to_mb),
    ]
