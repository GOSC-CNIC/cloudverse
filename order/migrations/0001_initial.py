# Generated by Django 4.2.4 on 2023-08-29 08:00

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(editable=False, max_length=32, primary_key=True, serialize=False, verbose_name='订单编号')),
                ('order_type', models.CharField(choices=[('new', '新购'), ('renewal', '续费'), ('upgrade', '升级'), ('downgrade', '降级'), ('post2pre', '按量付费转包年包月')], default='new', max_length=16, verbose_name='订单类型')),
                ('status', models.CharField(choices=[('paid', '已支付'), ('unpaid', '未支付'), ('cancelled', '作废'), ('refund', '全额退款'), ('partrefund', '部分退款'), ('refunding', '退款中')], default='paid', max_length=16, verbose_name='订单状态')),
                ('total_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), help_text='原价，折扣前的价格', max_digits=10, verbose_name='原价金额')),
                ('payable_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), help_text='需要支付的金额，扣除优惠或折扣后的金额', max_digits=10, verbose_name='应付金额')),
                ('pay_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), help_text='实际交易金额', max_digits=10, verbose_name='实付金额')),
                ('balance_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='余额支付金额')),
                ('coupon_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='券支付金额')),
                ('service_id', models.CharField(blank=True, default='', max_length=36, verbose_name='服务id')),
                ('service_name', models.CharField(blank=True, default='', max_length=255, verbose_name='服务名称')),
                ('resource_type', models.CharField(choices=[('vm', '云主机'), ('disk', '云硬盘'), ('bucket', '存储桶')], default='vm', max_length=16, verbose_name='资源类型')),
                ('instance_config', models.JSONField(blank=True, default=dict, verbose_name='资源的规格和配置')),
                ('period', models.IntegerField(blank=True, default=0, verbose_name='订购时长(月)')),
                ('payment_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='支付时间')),
                ('pay_type', models.CharField(choices=[('prepaid', '包年包月'), ('postpaid', '按量计费'), ('quota', '资源配额券')], max_length=16, verbose_name='结算方式')),
                ('payment_method', models.CharField(choices=[('unknown', '未知'), ('balance', '余额'), ('cashcoupon', '资源券'), ('mixed', '混合支付')], default='unknown', max_length=16, verbose_name='付款方式')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('start_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='起用时间')),
                ('end_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='终止时间')),
                ('user_id', models.CharField(blank=True, default='', max_length=36, verbose_name='用户ID')),
                ('username', models.CharField(blank=True, default='', max_length=64, verbose_name='用户名')),
                ('vo_id', models.CharField(blank=True, default='', max_length=36, verbose_name='VO组ID')),
                ('vo_name', models.CharField(blank=True, default='', max_length=256, verbose_name='VO组名')),
                ('owner_type', models.CharField(choices=[('user', '用户'), ('vo', 'VO组')], max_length=8, verbose_name='所有者类型')),
                ('completion_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='交易完成时间')),
                ('trading_status', models.CharField(choices=[('opening', '交易中'), ('undelivered', '订单资源交付失败'), ('completed', '交易成功'), ('closed', '交易关闭'), ('partdeliver', '部分交付失败')], default='opening', max_length=16, verbose_name='交易状态')),
                ('deleted', models.BooleanField(default=False, verbose_name='删除')),
                ('cancelled_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='作废时间')),
                ('app_service_id', models.CharField(blank=True, default='', max_length=36, verbose_name='app服务id')),
                ('payment_history_id', models.CharField(blank=True, default='', max_length=36, verbose_name='支付记录id')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'db_table': 'order',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(120)], verbose_name='月数')),
                ('enable', models.BooleanField(default=True, verbose_name='可用状态')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '订购时长',
                'verbose_name_plural': '订购时长',
                'db_table': 'order_period',
                'ordering': ['period'],
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_ram', models.DecimalField(decimal_places=5, help_text='内存每GiB每小时的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='内存GiB每小时')),
                ('vm_cpu', models.DecimalField(decimal_places=5, help_text='每个CPU每小时的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='每CPU每小时')),
                ('vm_pub_ip', models.DecimalField(decimal_places=5, help_text='每个公网IP每小时的保有费价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='每公网IP每小时保有费')),
                ('vm_disk', models.DecimalField(decimal_places=5, help_text='系统盘每GiB每小时的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='系统盘GiB每小时')),
                ('vm_disk_snap', models.DecimalField(decimal_places=5, help_text='系统盘快照每GiB每小时的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='系统盘快照GiB每小时')),
                ('vm_upstream', models.DecimalField(decimal_places=5, help_text='云主机上行流量每GiB的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='云主机上行流量每GiB')),
                ('vm_downstream', models.DecimalField(decimal_places=5, help_text='云主机下行流量每GiB的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='云主机下行流量每GiB')),
                ('disk_size', models.DecimalField(decimal_places=5, help_text='云盘每GiB每天的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='云盘GiB每天')),
                ('disk_snap', models.DecimalField(decimal_places=5, help_text='云盘快照每GiB每天的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='云盘快照GiB每天')),
                ('obj_size', models.DecimalField(decimal_places=5, help_text='对象存储每GiB每天的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='对象存储GiB每天')),
                ('obj_upstream', models.DecimalField(decimal_places=5, help_text='对象存储上行流量每GiB的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='对象存储上行流量每GiB')),
                ('obj_downstream', models.DecimalField(decimal_places=5, help_text='对象存储下行流量每GiB的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='对象存储下行流量每GiB')),
                ('obj_replication', models.DecimalField(decimal_places=5, help_text='对象存储同步流量每GiB的价格', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='对象存储同步流量每GiB')),
                ('obj_get_request', models.DecimalField(decimal_places=5, help_text='对象存储每万次get请求', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='对象存储每万次get请求')),
                ('obj_put_request', models.DecimalField(decimal_places=5, help_text='对象存储每万次put请求', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='对象存储每万次put请求')),
                ('prepaid_discount', models.PositiveSmallIntegerField(default=100, help_text='0-100, 包年包月预付费价格在按量计价的基础上按此折扣计价', validators=[django.core.validators.MaxValueValidator(100)], verbose_name='预付费折扣**%')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '资源计价定价',
                'verbose_name_plural': '资源计价定价',
                'db_table': 'price',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('vm', '云主机'), ('disk', '云硬盘'), ('bucket', '存储桶')], max_length=16, verbose_name='资源类型')),
                ('instance_id', models.CharField(blank=True, default='', max_length=36, verbose_name='资源实例id')),
                ('instance_status', models.CharField(choices=[('wait', '待交付'), ('success', '交付成功'), ('failed', '交付失败')], default='wait', max_length=16, verbose_name='资源交付结果')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('instance_remark', models.CharField(blank=True, default='', max_length=255, verbose_name='资源实例备注')),
                ('desc', models.CharField(blank=True, default='', max_length=255, verbose_name='资源交付结果描述')),
                ('last_deliver_time', models.DateTimeField(blank=True, default=None, help_text='用于记录上次交付资源的时间，防止并发重复交付', null=True, verbose_name='上次交付创建资源时间')),
                ('delivered_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='资源交付时间')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resource_set', to='order.order', verbose_name='订单')),
            ],
            options={
                'verbose_name': '订单资源',
                'verbose_name_plural': '订单资源',
                'db_table': 'order_resource',
                'ordering': ['-creation_time'],
            },
        ),
    ]
