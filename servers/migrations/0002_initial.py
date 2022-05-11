# Generated by Django 3.2.5 on 2022-05-11 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vo', '0001_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverarchive',
            name='archive_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='归档人'),
        ),
        migrations.AddField(
            model_name='serverarchive',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='server_archive_set', to='service.serviceconfig', verbose_name='接入的服务配置'),
        ),
        migrations.AddField(
            model_name='serverarchive',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_server_archives', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='serverarchive',
            name='vo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vo_server_archive_set', to='vo.virtualorganization', verbose_name='项目组'),
        ),
        migrations.AddField(
            model_name='server',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='server_set', to='service.serviceconfig', verbose_name='接入的服务配置'),
        ),
        migrations.AddField(
            model_name='server',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_servers', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='server',
            name='vo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vo_server_set', to='vo.virtualorganization', verbose_name='项目组'),
        ),
    ]