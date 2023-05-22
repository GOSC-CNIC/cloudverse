# Generated by Django 3.2.5 on 2022-05-11 08:39

from django.db import migrations, models
import django.db.models.deletion
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyOrganization',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('name_en', models.CharField(default='', max_length=255, verbose_name='英文名称')),
                ('abbreviation', models.CharField(default='', max_length=64, verbose_name='简称')),
                ('independent_legal_person', models.BooleanField(default=True, verbose_name='是否独立法人单位')),
                ('country', models.CharField(default='', max_length=128, verbose_name='国家/地区')),
                ('city', models.CharField(default='', max_length=128, verbose_name='城市')),
                ('postal_code', models.CharField(default='', max_length=32, verbose_name='邮政编码')),
                ('address', models.CharField(default='', max_length=256, verbose_name='单位地址')),
                ('endpoint_vms', models.CharField(blank=True, default=None, help_text='http(s)://{hostname}:{port}/', max_length=255, null=True, verbose_name='云主机服务地址url')),
                ('endpoint_object', models.CharField(blank=True, default=None, help_text='http(s)://{hostname}:{port}/', max_length=255, null=True, verbose_name='存储服务地址url')),
                ('endpoint_compute', models.CharField(blank=True, default=None, help_text='http(s)://{hostname}:{port}/', max_length=255, null=True, verbose_name='计算服务地址url')),
                ('endpoint_monitor', models.CharField(blank=True, default=None, help_text='http(s)://{hostname}:{port}/', max_length=255, null=True, verbose_name='检测报警服务地址url')),
                ('creation_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('status', models.CharField(choices=[('wait', '待审批'), ('cancel', '取消申请'), ('pending', '审批中'), ('reject', '拒绝'), ('pass', '通过')], default='wait', max_length=16, verbose_name='状态')),
                ('desc', models.CharField(blank=True, max_length=255, verbose_name='描述')),
                ('logo_url', models.CharField(blank=True, default='', max_length=256, verbose_name='LOGO url')),
                ('certification_url', models.CharField(blank=True, default='', max_length=256, verbose_name='机构认证代码url')),
                ('deleted', models.BooleanField(default=False, verbose_name='删除')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='经度')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='纬度')),
            ],
            options={
                'verbose_name': '机构加入申请',
                'verbose_name_plural': '机构加入申请',
                'db_table': 'organization_apply',
                'ordering': ['creation_time'],
            },
        ),
        migrations.CreateModel(
            name='ApplyVmService',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('evcloud', 'EVCloud'), ('openstack', 'OpenStack'), ('vmware', 'VMware'), ('aliyun', '阿里云'), ('unis-cloud', '紫光云')], default='evcloud', max_length=32, verbose_name='服务平台类型')),
                ('cloud_type', models.CharField(choices=[('public', '公有云'), ('private', '私有云'), ('hybrid', '混合云')], default='private', max_length=32, verbose_name='云服务类型')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('approve_time', models.DateTimeField(auto_now_add=True, verbose_name='审批时间')),
                ('status', models.CharField(choices=[('wait', '待审核'), ('cancel', '取消申请'), ('pending', '审核中'), ('first_pass', '初审通过'), ('first_reject', '初审拒绝'), ('test_failed', '测试未通过'), ('test_pass', '测试通过'), ('reject', '拒绝'), ('pass', '通过')], default='wait', max_length=16, verbose_name='状态')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='经度')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='纬度')),
                ('name', models.CharField(max_length=255, verbose_name='服务名称')),
                ('name_en', models.CharField(default='', max_length=255, verbose_name='英文名称')),
                ('region', models.CharField(blank=True, default='', help_text='OpenStack服务区域名称,EVCloud分中心ID', max_length=128, verbose_name='服务区域')),
                ('endpoint_url', models.CharField(help_text='http(s)://{hostname}:{port}/', max_length=255, unique=True, verbose_name='服务地址url')),
                ('api_version', models.CharField(default='v3', help_text='预留，主要EVCloud使用', max_length=64, verbose_name='API版本')),
                ('username', models.CharField(help_text='用于此服务认证的用户名', max_length=128, verbose_name='用户名')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('project_name', models.CharField(blank=True, default='', help_text='only required when OpenStack', max_length=128, verbose_name='Project Name')),
                ('project_domain_name', models.CharField(blank=True, default='', help_text='only required when OpenStack', max_length=128, verbose_name='Project Domain Name')),
                ('user_domain_name', models.CharField(blank=True, default='', help_text='only required when OpenStack', max_length=128, verbose_name='User Domain Name')),
                ('remarks', models.CharField(blank=True, default='', max_length=255, verbose_name='备注')),
                ('need_vpn', models.BooleanField(default=True, verbose_name='是否需要VPN')),
                ('vpn_endpoint_url', models.CharField(blank=True, default='', help_text='http(s)://{hostname}:{port}/', max_length=255, verbose_name='VPN服务地址url')),
                ('vpn_api_version', models.CharField(blank=True, default='v3', max_length=64, verbose_name='VPN API版本')),
                ('vpn_username', models.CharField(blank=True, default='', help_text='用于VPN服务认证的用户名', max_length=128, verbose_name='用户名')),
                ('vpn_password', models.CharField(blank=True, default='', max_length=255, verbose_name='密码')),
                ('deleted', models.BooleanField(default=False, verbose_name='删除')),
                ('contact_person', models.CharField(blank=True, default='', max_length=128, verbose_name='联系人')),
                ('contact_email', models.EmailField(blank=True, default='', max_length=254, verbose_name='联系人邮箱')),
                ('contact_telephone', models.CharField(blank=True, default='', max_length=16, verbose_name='联系人电话')),
                ('contact_fixed_phone', models.CharField(blank=True, default='', max_length=16, verbose_name='联系人固定电话')),
                ('contact_address', models.CharField(blank=True, default='', max_length=256, verbose_name='联系人地址')),
                ('logo_url', models.CharField(blank=True, default='', max_length=256, verbose_name='LOGO url')),
            ],
            options={
                'verbose_name': 'VM服务单元接入申请',
                'verbose_name_plural': 'VM服务单元接入申请',
                'db_table': 'vm_service_apply',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='DataCenter',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('name_en', models.CharField(default='', max_length=255, verbose_name='英文名称')),
                ('abbreviation', models.CharField(default='', max_length=64, verbose_name='简称')),
                ('independent_legal_person', models.BooleanField(default=True, verbose_name='是否独立法人单位')),
                ('country', models.CharField(default='', max_length=128, verbose_name='国家/地区')),
                ('city', models.CharField(default='', max_length=128, verbose_name='城市')),
                ('postal_code', models.CharField(default='', max_length=32, verbose_name='邮政编码')),
                ('address', models.CharField(default='', max_length=256, verbose_name='单位地址')),
                ('endpoint_vms', models.CharField(blank=True, default=None, help_text='http(s)://{hostname}:{port}/', max_length=255, null=True, verbose_name='云主机服务地址url')),
                ('endpoint_object', models.CharField(blank=True, default=None, help_text='http(s)://{hostname}:{port}/', max_length=255, null=True, verbose_name='存储服务地址url')),
                ('endpoint_compute', models.CharField(blank=True, default=None, help_text='http(s)://{hostname}:{port}/', max_length=255, null=True, verbose_name='计算服务地址url')),
                ('endpoint_monitor', models.CharField(blank=True, default=None, help_text='http(s)://{hostname}:{port}/', max_length=255, null=True, verbose_name='检测报警服务地址url')),
                ('creation_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='创建时间')),
                ('status', models.SmallIntegerField(choices=[(1, '开启状态'), (2, '关闭状态')], default=1, verbose_name='服务状态')),
                ('desc', models.CharField(blank=True, max_length=255, verbose_name='描述')),
                ('logo_url', models.CharField(blank=True, default='', max_length=256, verbose_name='LOGO url')),
                ('certification_url', models.CharField(blank=True, default='', max_length=256, verbose_name='机构认证代码url')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='经度')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='纬度')),
            ],
            options={
                'verbose_name': '机构',
                'verbose_name_plural': '机构',
                'ordering': ['creation_time'],
            },
        ),
        migrations.CreateModel(
            name='ServiceConfig',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('evcloud', 'EVCloud'), ('openstack', 'OpenStack'), ('vmware', 'VMware'), ('aliyun', '阿里云'), ('unis-cloud', '紫光云')], default='evcloud', max_length=32, verbose_name='服务平台类型')),
                ('cloud_type', models.CharField(choices=[('public', '公有云'), ('private', '私有云'), ('hybrid', '混合云')], default='private', max_length=32, verbose_name='云服务类型')),
                ('name', models.CharField(max_length=255, verbose_name='服务名称')),
                ('name_en', models.CharField(default='', max_length=255, verbose_name='服务英文名称')),
                ('region_id', models.CharField(blank=True, default='', max_length=128, verbose_name='服务区域/分中心ID')),
                ('endpoint_url', models.CharField(help_text='http(s)://{hostname}:{port}/', max_length=255, unique=True, verbose_name='服务地址url')),
                ('api_version', models.CharField(default='v3', help_text='预留，主要EVCloud使用', max_length=64, verbose_name='API版本')),
                ('username', models.CharField(help_text='用于此服务认证的用户名', max_length=128, verbose_name='用户名')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('status', models.CharField(choices=[('enable', '服务中'), ('disable', '停止服务'), ('deleted', '删除')], default='enable', max_length=32, verbose_name='服务状态')),
                ('remarks', models.CharField(blank=True, default='', max_length=255, verbose_name='备注')),
                ('need_vpn', models.BooleanField(default=True, verbose_name='是否需要VPN')),
                ('vpn_endpoint_url', models.CharField(blank=True, default='', help_text='http(s)://{hostname}:{port}/', max_length=255, verbose_name='VPN服务地址url')),
                ('vpn_api_version', models.CharField(blank=True, default='v3', help_text='预留，主要EVCloud使用', max_length=64, verbose_name='VPN服务API版本')),
                ('vpn_username', models.CharField(blank=True, default='', help_text='用于此服务认证的用户名', max_length=128, verbose_name='VPN服务用户名')),
                ('vpn_password', models.CharField(blank=True, default='', max_length=255, verbose_name='VPN服务密码')),
                ('extra', models.CharField(blank=True, default='', help_text='json格式', max_length=1024, validators=[utils.validators.JSONStringValidator()], verbose_name='其他配置')),
                ('contact_person', models.CharField(blank=True, default='', max_length=128, verbose_name='联系人名称')),
                ('contact_email', models.EmailField(blank=True, default='', max_length=254, verbose_name='联系人邮箱')),
                ('contact_telephone', models.CharField(blank=True, default='', max_length=16, verbose_name='联系人电话')),
                ('contact_fixed_phone', models.CharField(blank=True, default='', max_length=16, verbose_name='联系人固定电话')),
                ('contact_address', models.CharField(blank=True, default='', max_length=256, verbose_name='联系人地址')),
                ('logo_url', models.CharField(blank=True, default='', max_length=256, verbose_name='LOGO url')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='经度')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='纬度')),
                ('data_center', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_set', to='service.datacenter', verbose_name='数据中心')),
            ],
            options={
                'verbose_name': '服务单元接入配置',
                'verbose_name_plural': '服务单元接入配置',
                'ordering': ['-add_time'],
            },
        ),
        migrations.CreateModel(
            name='ServiceShareQuota',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_ip_total', models.IntegerField(default=0, verbose_name='总私网IP数')),
                ('private_ip_used', models.IntegerField(default=0, verbose_name='已用私网IP数')),
                ('public_ip_total', models.IntegerField(default=0, verbose_name='总公网IP数')),
                ('public_ip_used', models.IntegerField(default=0, verbose_name='已用公网IP数')),
                ('vcpu_total', models.IntegerField(default=0, verbose_name='总CPU核数')),
                ('vcpu_used', models.IntegerField(default=0, verbose_name='已用CPU核数')),
                ('ram_total', models.IntegerField(default=0, verbose_name='总内存大小(GB)')),
                ('ram_used', models.IntegerField(default=0, verbose_name='已用内存大小(GB)')),
                ('disk_size_total', models.IntegerField(default=0, verbose_name='总硬盘大小(GB)')),
                ('disk_size_used', models.IntegerField(default=0, verbose_name='已用硬盘大小(GB)')),
                ('creation_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('enable', models.BooleanField(default=True, help_text='选中，资源配额生效；未选中，无法申请分中心资源', verbose_name='有效状态')),
                ('service', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_share_quota', to='service.serviceconfig', verbose_name='接入服务')),
            ],
            options={
                'verbose_name': '云主机服务单元的分享资源配额',
                'verbose_name_plural': '云主机服务单元的分享资源配额',
                'db_table': 'service_share_quota',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='ServicePrivateQuota',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_ip_total', models.IntegerField(default=0, verbose_name='总私网IP数')),
                ('private_ip_used', models.IntegerField(default=0, verbose_name='已用私网IP数')),
                ('public_ip_total', models.IntegerField(default=0, verbose_name='总公网IP数')),
                ('public_ip_used', models.IntegerField(default=0, verbose_name='已用公网IP数')),
                ('vcpu_total', models.IntegerField(default=0, verbose_name='总CPU核数')),
                ('vcpu_used', models.IntegerField(default=0, verbose_name='已用CPU核数')),
                ('ram_total', models.IntegerField(default=0, verbose_name='总内存大小(GB)')),
                ('ram_used', models.IntegerField(default=0, verbose_name='已用内存大小(GB)')),
                ('disk_size_total', models.IntegerField(default=0, verbose_name='总硬盘大小(GB)')),
                ('disk_size_used', models.IntegerField(default=0, verbose_name='已用硬盘大小(GB)')),
                ('creation_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('enable', models.BooleanField(default=True, help_text='选中，资源配额生效；未选中，无法申请分中心资源', verbose_name='有效状态')),
                ('service', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_private_quota', to='service.serviceconfig', verbose_name='接入服务')),
            ],
            options={
                'verbose_name': '云主机服务单元的私有资源配额',
                'verbose_name_plural': '云主机服务单元的私有资源配额',
                'db_table': 'service_private_quota',
                'ordering': ['-creation_time'],
            },
        ),
    ]
