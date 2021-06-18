# Generated by Django 3.2.4 on 2021-06-17 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0001_squashed_0006_userquota_deleted_squashed_0009_rename_data_center_applyvmservice_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquota',
            name='vo',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vo_quota_set', to='vo.virtualorganization', verbose_name='项目组'),
        ),
        migrations.AlterField(
            model_name='userquota',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_quota', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
