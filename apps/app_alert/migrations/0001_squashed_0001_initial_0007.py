# Generated by Django 4.2.9 on 2024-05-14 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    # replaces = [('app_alert', '0001_initial'), ('app_alert', '0002_scriptflagmodel'),
    #             ('app_alert', '0003_delete_scriptflagmodel'),
    #             ('app_alert', '0004_alter_alertworkorder_creation_and_more'),
    #             ('app_alert', '0005_alter_alertworkorder_status'),
    #             ('app_alert', '0006_alter_alertlifetimemodel_end_and_more'),
    #             ('app_alert', '0007_delete_alertwhitelistmodel')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertLifetimeModel',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('firing', '进行中'), ('resolved', '已恢复'), ('work order', '工单处理')], max_length=20, verbose_name='告警状态')),
                ('start', models.PositiveBigIntegerField(db_index=True, null=True, verbose_name='告警开始时间')),
                ('end', models.PositiveBigIntegerField(db_index=True, null=True, verbose_name='告警结束时间')),
            ],
            options={
                'verbose_name': '告警生命周期',
                'verbose_name_plural': '告警生命周期',
                'db_table': 'alert_lifetime',
                'ordering': ['-start'],
            },
        ),
        migrations.CreateModel(
            name='AlertModel',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('fingerprint', models.CharField(db_index=True, max_length=40, unique=True, verbose_name='指纹')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('type', models.CharField(max_length=255, verbose_name='类型')),
                ('instance', models.CharField(db_index=True, default='', max_length=100, verbose_name='告警实例')),
                ('port', models.CharField(db_index=True, default='', max_length=100, verbose_name='告警端口')),
                ('cluster', models.CharField(db_index=True, max_length=50, verbose_name='集群名称')),
                ('severity', models.CharField(max_length=50, verbose_name='级别')),
                ('summary', models.TextField(verbose_name='摘要')),
                ('description', models.TextField(verbose_name='详情')),
                ('start', models.PositiveBigIntegerField(db_index=True, verbose_name='告警开始时间')),
                ('end', models.PositiveBigIntegerField(db_index=True, null=True, verbose_name='告警结束时间')),
                ('count', models.PositiveBigIntegerField(default=1, verbose_name='累加条数')),
                ('first_notification', models.PositiveBigIntegerField(null=True, verbose_name='首次通知时间')),
                ('last_notification', models.PositiveBigIntegerField(null=True, verbose_name='上次通知时间')),
                ('creation', models.PositiveBigIntegerField(null=True, verbose_name='创建时间')),
                ('modification', models.PositiveBigIntegerField(null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '进行中告警',
                'verbose_name_plural': '进行中告警',
                'db_table': 'alert_firing',
                'ordering': ['-start'],
            },
        ),
        migrations.CreateModel(
            name='PreAlertModel',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('fingerprint', models.CharField(db_index=True, max_length=40, unique=True, verbose_name='指纹')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('type', models.CharField(max_length=255, verbose_name='类型')),
                ('instance', models.CharField(db_index=True, default='', max_length=100, verbose_name='告警实例')),
                ('port', models.CharField(db_index=True, default='', max_length=100, verbose_name='告警端口')),
                ('cluster', models.CharField(db_index=True, max_length=50, verbose_name='集群名称')),
                ('severity', models.CharField(max_length=50, verbose_name='级别')),
                ('summary', models.TextField(verbose_name='摘要')),
                ('description', models.TextField(verbose_name='详情')),
                ('start', models.PositiveBigIntegerField(db_index=True, verbose_name='告警开始时间')),
                ('end', models.PositiveBigIntegerField(db_index=True, null=True, verbose_name='告警结束时间')),
                ('count', models.PositiveBigIntegerField(default=1, verbose_name='累加条数')),
                ('first_notification', models.PositiveBigIntegerField(null=True, verbose_name='首次通知时间')),
                ('last_notification', models.PositiveBigIntegerField(null=True, verbose_name='上次通知时间')),
                ('creation', models.PositiveBigIntegerField(null=True, verbose_name='创建时间')),
                ('modification', models.PositiveBigIntegerField(null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '预处理告警',
                'verbose_name_plural': '预处理告警',
                'db_table': 'alert_prepare',
                'ordering': ['-start'],
            },
        ),
        migrations.CreateModel(
            name='ResolvedAlertModel',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('type', models.CharField(max_length=255, verbose_name='类型')),
                ('instance', models.CharField(db_index=True, default='', max_length=100, verbose_name='告警实例')),
                ('port', models.CharField(db_index=True, default='', max_length=100, verbose_name='告警端口')),
                ('cluster', models.CharField(db_index=True, max_length=50, verbose_name='集群名称')),
                ('severity', models.CharField(max_length=50, verbose_name='级别')),
                ('summary', models.TextField(verbose_name='摘要')),
                ('description', models.TextField(verbose_name='详情')),
                ('start', models.PositiveBigIntegerField(db_index=True, verbose_name='告警开始时间')),
                ('end', models.PositiveBigIntegerField(db_index=True, null=True, verbose_name='告警结束时间')),
                ('count', models.PositiveBigIntegerField(default=1, verbose_name='累加条数')),
                ('first_notification', models.PositiveBigIntegerField(null=True, verbose_name='首次通知时间')),
                ('last_notification', models.PositiveBigIntegerField(null=True, verbose_name='上次通知时间')),
                ('creation', models.PositiveBigIntegerField(null=True, verbose_name='创建时间')),
                ('modification', models.PositiveBigIntegerField(null=True, verbose_name='更新时间')),
                ('fingerprint', models.CharField(db_index=True, max_length=40, verbose_name='指纹')),
            ],
            options={
                'verbose_name': '已恢复告警',
                'verbose_name_plural': '已恢复告警',
                'db_table': 'alert_resolved',
                'ordering': ['-start'],
                'unique_together': {('fingerprint', 'start')},
            },
        ),
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert', models.CharField(db_index=True, max_length=40, verbose_name='告警ID')),
                ('email', models.CharField(db_index=True, max_length=100, verbose_name='邮箱')),
                ('timestamp', models.PositiveBigIntegerField(db_index=True, verbose_name='通知时间')),
            ],
            options={
                'verbose_name': '邮件通知记录',
                'verbose_name_plural': '邮件通知记录',
                'db_table': 'alert_email_notification',
                'ordering': ['-timestamp', 'email'],
                'unique_together': {('alert', 'email', 'timestamp')},
            },
        ),
        migrations.CreateModel(
            name='AlertMonitorJobServer',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, verbose_name='监控的主机集群名称')),
                ('name_en', models.CharField(default='', max_length=255, verbose_name='监控的主机集群英文名称')),
                ('job_tag', models.CharField(default='', help_text='模板：xxx_node_metric', max_length=255, verbose_name='主机集群标签名称')),
                ('prometheus', models.CharField(blank=True, default='', help_text='http(s)://example.cn/', max_length=255, verbose_name='Prometheus接口')),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('remark', models.TextField(blank=True, default='', verbose_name='备注')),
                ('sort_weight', models.IntegerField(default=0, help_text='值越小排序越靠前', verbose_name='排序值')),
                ('grafana_url', models.CharField(blank=True, default='', max_length=255, verbose_name='Grafana连接')),
                ('dashboard_url', models.CharField(blank=True, default='', max_length=255, verbose_name='Dashboard连接')),
                ('users', models.ManyToManyField(blank=True, db_constraint=False, db_table='alert_server_users', related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='管理用户')),
            ],
            options={
                'verbose_name': '告警集群',
                'verbose_name_plural': '告警集群',
                'db_table': 'alert_monitorjobserver',
                'ordering': ['-creation'],
            },
        ),
        migrations.CreateModel(
            name='AlertWorkOrder',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect', models.CharField(max_length=40, verbose_name='集合ID')),
                ('status', models.CharField(choices=[('无需处理', '无需处理'), ('已完成', '已完成'), ('误报', '误报')], default='无需处理', max_length=10, verbose_name='状态')),
                ('remark', models.TextField(blank=True, default='', verbose_name='备注')),
                ('creation', models.PositiveBigIntegerField(null=True, verbose_name='创建时间')),
                ('modification', models.PositiveBigIntegerField(null=True, verbose_name='更新时间')),
                ('alert', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='work_order', to='app_alert.alertmodel', verbose_name='告警')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='work_order', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '告警工单',
                'verbose_name_plural': '告警工单',
                'db_table': 'alert_work_order',
                'ordering': ['-creation'],
                'unique_together': {('collect', 'alert')},
            },
        ),
    ]
