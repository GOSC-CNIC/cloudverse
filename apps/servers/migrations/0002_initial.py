# Generated by Django 4.2.4 on 2023-08-29 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0004_orgdatacenter_serviceconfig_org_data_center'),
        ('servers', '0001_initial'),
        ('vo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceconfig',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='service_set', to=settings.AUTH_USER_MODEL,
                                         verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='serviceconfig',
            name='org_data_center',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                    to='service.orgdatacenter', verbose_name='数据中心'),
        ),
        migrations.CreateModel(
            name='ApplyVmService',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('service_type', models.CharField(
                    choices=[('evcloud', 'EVCloud'), ('openstack', 'OpenStack'), ('vmware', 'VMware'),
                             ('aliyun', '阿里云'), ('unis-cloud', '紫光云')], default='evcloud', max_length=32,
                    verbose_name='服务平台类型')),
                ('cloud_type',
                 models.CharField(choices=[('public', '公有云'), ('private', '私有云'), ('hybrid', '混合云')], default='private',
                                  max_length=32, verbose_name='云服务类型')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('approve_time', models.DateTimeField(auto_now_add=True, verbose_name='审批时间')),
                ('status', models.CharField(
                    choices=[('wait', '待审核'), ('cancel', '取消申请'), ('pending', '审核中'), ('first_pass', '初审通过'),
                             ('first_reject', '初审拒绝'), ('test_failed', '测试未通过'), ('test_pass', '测试通过'),
                             ('reject', '拒绝'), ('pass', '通过')], default='wait', max_length=16, verbose_name='状态')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='经度')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='纬度')),
                ('name', models.CharField(max_length=255, verbose_name='服务名称')),
                ('name_en', models.CharField(default='', max_length=255, verbose_name='英文名称')),
                ('region',
                 models.CharField(blank=True, default='', help_text='OpenStack服务区域名称,EVCloud分中心ID', max_length=128,
                                  verbose_name='服务区域')),
                ('endpoint_url', models.CharField(help_text='http(s)://{hostname}:{port}/', max_length=255, unique=True,
                                                  verbose_name='服务地址url')),
                ('api_version',
                 models.CharField(default='v3', help_text='预留，主要EVCloud使用', max_length=64, verbose_name='API版本')),
                ('username', models.CharField(help_text='用于此服务认证的用户名', max_length=128, verbose_name='用户名')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('project_name',
                 models.CharField(blank=True, default='', help_text='only required when OpenStack', max_length=128,
                                  verbose_name='Project Name')),
                ('project_domain_name',
                 models.CharField(blank=True, default='', help_text='only required when OpenStack', max_length=128,
                                  verbose_name='Project Domain Name')),
                ('user_domain_name',
                 models.CharField(blank=True, default='', help_text='only required when OpenStack', max_length=128,
                                  verbose_name='User Domain Name')),
                ('remarks', models.CharField(blank=True, default='', max_length=255, verbose_name='备注')),
                ('need_vpn', models.BooleanField(default=True, verbose_name='是否需要VPN')),
                ('vpn_endpoint_url',
                 models.CharField(blank=True, default='', help_text='http(s)://{hostname}:{port}/', max_length=255,
                                  verbose_name='VPN服务地址url')),
                (
                'vpn_api_version', models.CharField(blank=True, default='v3', max_length=64, verbose_name='VPN API版本')),
                ('vpn_username', models.CharField(blank=True, default='', help_text='用于VPN服务认证的用户名', max_length=128,
                                                  verbose_name='用户名')),
                ('vpn_password', models.CharField(blank=True, default='', max_length=255, verbose_name='密码')),
                ('deleted', models.BooleanField(default=False, verbose_name='删除')),
                ('contact_person', models.CharField(blank=True, default='', max_length=128, verbose_name='联系人')),
                ('contact_email', models.EmailField(blank=True, default='', max_length=254, verbose_name='联系人邮箱')),
                ('contact_telephone', models.CharField(blank=True, default='', max_length=16, verbose_name='联系人电话')),
                (
                'contact_fixed_phone', models.CharField(blank=True, default='', max_length=16, verbose_name='联系人固定电话')),
                ('contact_address', models.CharField(blank=True, default='', max_length=256, verbose_name='联系人地址')),
                ('logo_url', models.CharField(blank=True, default='', max_length=256, verbose_name='LOGO url')),
                ('organization',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.datacenter',
                                   verbose_name='数据中心')),
                ('service', models.OneToOneField(
                    blank=True, default=None, help_text='服务接入申请审批通过后生成的对应的接入服务', null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='apply_service', to='servers.serviceconfig', verbose_name='接入服务')),
                ('user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL,
                                   verbose_name='申请用户')),
            ],
            options={
                'verbose_name': 'VM服务单元接入申请',
                'verbose_name_plural': 'VM服务单元接入申请',
                'db_table': 'vm_service_apply',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.AddField(
            model_name='serverarchive',
            name='archive_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='归档人'),
        ),
        migrations.AddField(
            model_name='serverarchive',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='server_archive_set', to='servers.serviceconfig', verbose_name='接入的服务配置'),
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
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='server_set', to='servers.serviceconfig', verbose_name='接入的服务配置'),
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
        migrations.AddField(
            model_name='flavor',
            name='service',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='servers.serviceconfig', verbose_name='服务单元'),
        ),
        migrations.AddField(
            model_name='diskchangelog',
            name='service',
            field=models.ForeignKey(db_constraint=False, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='servers.serviceconfig', verbose_name='服务单元'),
        ),
        migrations.AddField(
            model_name='diskchangelog',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='diskchangelog',
            name='vo',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='vo.virtualorganization', verbose_name='项目组'),
        ),
        migrations.AddField(
            model_name='disk',
            name='server',
            field=models.ForeignKey(blank=True, db_constraint=False, db_index=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mounted_disk_set', to='servers.server', verbose_name='挂载于云主机'),
        ),
        migrations.AddField(
            model_name='disk',
            name='service',
            field=models.ForeignKey(db_constraint=False, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='servers.serviceconfig', verbose_name='服务单元'),
        ),
        migrations.AddField(
            model_name='disk',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='disk',
            name='vo',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='vo.virtualorganization', verbose_name='项目组'),
        ),
        migrations.AddIndex(
            model_name='diskchangelog',
            index=models.Index(fields=['disk_id'], name='idx_disk_id'),
        ),
    ]