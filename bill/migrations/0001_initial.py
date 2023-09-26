# Generated by Django 4.2.4 on 2023-08-29 08:00

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashCoupon',
            fields=[
                ('face_value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='面额')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('effective_time', models.DateTimeField(verbose_name='生效时间')),
                ('expiration_time', models.DateTimeField(verbose_name='过期时间')),
                ('id', models.CharField(editable=False, max_length=32, primary_key=True, serialize=False, verbose_name='编码')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='余额')),
                ('status', models.CharField(choices=[('wait', '未领取'), ('available', '有效'), ('cancelled', '作废'), ('deleted', '删除')], default='wait', max_length=16, verbose_name='状态')),
                ('granted_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='领取/发放时间')),
                ('owner_type', models.CharField(blank=True, choices=[('user', '用户'), ('vo', 'VO组'), ('', '未知')], default='', max_length=16, verbose_name='所属类型')),
                ('_coupon_code', models.CharField(db_column='coupon_code', max_length=64, verbose_name='券密码')),
                ('issuer', models.CharField(blank=True, default='', max_length=128, verbose_name='发放人')),
                ('balance_notice_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='余额不足通知时间')),
                ('expire_notice_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='过期通知时间')),
            ],
            options={
                'verbose_name': '资源券',
                'verbose_name_plural': '资源券',
                'db_table': 'cash_coupon',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='CashCouponActivity',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='面额')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('effective_time', models.DateTimeField(verbose_name='生效时间')),
                ('expiration_time', models.DateTimeField(verbose_name='过期时间')),
                ('name', models.CharField(max_length=255, verbose_name='活动名称')),
                ('grant_total', models.IntegerField(default=0, verbose_name='发放总数量')),
                ('granted_count', models.IntegerField(default=0, verbose_name='已发放数量')),
                ('grant_status', models.CharField(choices=[('wait', '待发放'), ('grant', '发放中'), ('completed', '发放完毕')], default='wait', max_length=16, verbose_name='发放状态')),
                ('desc', models.CharField(blank=True, default='', max_length=255, verbose_name='描述信息')),
                ('creator', models.CharField(blank=True, default='', max_length=128, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '资源券活动/模板',
                'verbose_name_plural': '资源券活动/模板',
                'db_table': 'cash_coupon_activity',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='CashCouponPaymentHistory',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('amounts', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='金额')),
                ('before_payment', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='支付前余额')),
                ('after_payment', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='支付后余额')),
            ],
            options={
                'verbose_name': '资源券扣费记录',
                'verbose_name_plural': '资源券扣费记录',
                'db_table': 'cash_coupon_payment',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='PayApp',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='应用名称')),
                ('app_url', models.CharField(blank=True, default='', max_length=256, verbose_name='应用网址')),
                ('app_desc', models.CharField(blank=True, default='', max_length=1024, verbose_name='应用描述')),
                ('rsa_public_key', models.CharField(blank=True, default='', max_length=2000, verbose_name='RSA公钥')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.CharField(choices=[('unaudited', '未审核'), ('normal', '正常'), ('ban', '禁止')], default='unaudited', max_length=16, verbose_name='应用状态')),
            ],
            options={
                'verbose_name': '支付应用APP',
                'verbose_name_plural': '支付应用APP',
                'db_table': 'app',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='PayAppService',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='服务名称')),
                ('name_en', models.CharField(default='', max_length=255, verbose_name='服务英文名称')),
                ('resources', models.CharField(default='', max_length=128, verbose_name='服务提供的资源')),
                ('desc', models.CharField(blank=True, default='', max_length=1024, verbose_name='服务描述')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.CharField(choices=[('unaudited', '未审核'), ('normal', '正常'), ('ban', '禁止')], default='unaudited', max_length=16, verbose_name='服务状态')),
                ('contact_person', models.CharField(blank=True, default='', max_length=128, verbose_name='联系人名称')),
                ('contact_email', models.EmailField(blank=True, default='', max_length=254, verbose_name='联系人邮箱')),
                ('contact_telephone', models.CharField(blank=True, default='', max_length=16, verbose_name='联系人电话')),
                ('contact_fixed_phone', models.CharField(blank=True, default='', max_length=16, verbose_name='联系人固定电话')),
                ('contact_address', models.CharField(blank=True, default='', max_length=256, verbose_name='联系人地址')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='经度')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='纬度')),
                ('category', models.CharField(choices=[('vms-server', 'VMS云服务器'), ('vms-object', 'VMS对象存储'), ('vms-monitor', 'VMS监控'), ('high-cloud', '高等级云'), ('hpc', '高性能计算'), ('other', '其他')], default='other', max_length=16, verbose_name='服务类别')),
                ('service_id', models.CharField(blank=True, default='', max_length=64, verbose_name='对应的服务单元ID')),
            ],
            options={
                'verbose_name': '应用APP子服务',
                'verbose_name_plural': '应用APP子服务',
                'db_table': 'app_service',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_account', models.CharField(blank=True, default='', help_text='用户或VO余额ID, 及可能支持的其他账户', max_length=36, verbose_name='付款账户')),
                ('payment_method', models.CharField(choices=[('balance', '余额'), ('coupon', '资源券'), ('balance+coupon', '余额+资源券')], default='balance', max_length=16, verbose_name='付款方式')),
                ('executor', models.CharField(blank=True, default='', help_text='记录此次支付交易是谁执行完成的', max_length=128, verbose_name='交易执行人')),
                ('payer_id', models.CharField(blank=True, default='', help_text='user id or vo id', max_length=36, verbose_name='付款人ID')),
                ('payer_name', models.CharField(blank=True, default='', help_text='username or vo name', max_length=255, verbose_name='付款人名称')),
                ('payer_type', models.CharField(choices=[('user', '用户'), ('vo', 'VO组')], max_length=8, verbose_name='付款人类型')),
                ('payable_amounts', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='需付金额')),
                ('amounts', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='金额')),
                ('coupon_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), help_text='资源券或者抵扣金额', max_digits=10, verbose_name='券金额')),
                ('creation_time', models.DateTimeField(verbose_name='创建时间')),
                ('payment_time', models.DateTimeField(default=None, null=True, verbose_name='支付时间')),
                ('status', models.CharField(choices=[('wait', '等待支付'), ('success', '支付成功'), ('error', '支付失败'), ('closed', '交易关闭')], default='wait', max_length=16, verbose_name='支付状态')),
                ('status_desc', models.CharField(default='', max_length=255, verbose_name='支付状态描述')),
                ('subject', models.CharField(default='', max_length=256, verbose_name='标题')),
                ('remark', models.CharField(blank=True, default='', max_length=255, verbose_name='备注信息')),
                ('order_id', models.CharField(blank=True, default='', max_length=36, verbose_name='订单ID')),
                ('app_service_id', models.CharField(blank=True, default='', max_length=36, verbose_name='APP服务ID')),
                ('app_id', models.CharField(blank=True, default='', max_length=36, verbose_name='应用ID')),
                ('instance_id', models.CharField(default='', help_text='云主机，硬盘id，存储桶名称', max_length=64, verbose_name='资源实例ID')),
            ],
            options={
                'verbose_name': '支付记录',
                'verbose_name_plural': '支付记录',
                'db_table': 'payment_history',
                'ordering': ['-payment_time'],
            },
        ),
        migrations.CreateModel(
            name='PayOrgnazition',
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
                ('creation_time', models.DateTimeField(blank=True, default=None, null=True, verbose_name='创建时间')),
                ('desc', models.CharField(blank=True, max_length=255, verbose_name='描述')),
                ('logo_url', models.CharField(blank=True, default='', max_length=256, verbose_name='LOGO url')),
                ('certification_url', models.CharField(blank=True, default='', max_length=256, verbose_name='机构认证代码url')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='经度')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='纬度')),
            ],
            options={
                'verbose_name': '机构',
                'verbose_name_plural': '机构',
                'db_table': 'pay_orgnazition',
                'ordering': ['creation_time'],
            },
        ),
        migrations.CreateModel(
            name='Recharge',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_channel', models.CharField(choices=[('manual', '人工充值'), ('wechat', '微信支付'), ('alipay', '支付宝')], default='manual', max_length=16, verbose_name='交易渠道')),
                ('out_trade_no', models.CharField(blank=True, default='', max_length=64, verbose_name='外部交易编号')),
                ('channel_account', models.CharField(blank=True, default='', max_length=64, verbose_name='交易渠道账户编号')),
                ('channel_fee', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='交易渠道费用')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='充值总金额')),
                ('receipt_amount', models.DecimalField(decimal_places=2, help_text='交易渠道中我方账户实际收到的款项', max_digits=10, verbose_name='实收金额')),
                ('creation_time', models.DateTimeField(verbose_name='创建时间')),
                ('success_time', models.DateTimeField(default=None, null=True, verbose_name='充值成功时间')),
                ('status', models.CharField(choices=[('wait', '待充值'), ('success', '支付成功'), ('error', '支付失败'), ('closed', '交易关闭'), ('complete', '充值完成')], default='wait', max_length=16, verbose_name='充值状态')),
                ('status_desc', models.CharField(default='', max_length=255, verbose_name='充值状态描述')),
                ('in_account', models.CharField(blank=True, default='', help_text='用户或VO余额ID, 及可能支持的其他账户', max_length=36, verbose_name='入账账户')),
                ('owner_id', models.CharField(blank=True, default='', help_text='user id or vo id', max_length=36, verbose_name='所属人ID')),
                ('owner_name', models.CharField(blank=True, default='', help_text='username or vo name', max_length=255, verbose_name='所属人名称')),
                ('owner_type', models.CharField(choices=[('user', '用户'), ('vo', 'VO组')], max_length=8, verbose_name='所属人类型')),
                ('remark', models.CharField(default='', max_length=256, verbose_name='备注信息')),
                ('executor', models.CharField(blank=True, default='', help_text='记录此次支付交易是谁执行完成的', max_length=128, verbose_name='交易执行人')),
            ],
            options={
                'verbose_name': '充值记录',
                'verbose_name_plural': '充值记录',
                'db_table': 'wallet_recharge',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='RefundRecord',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_id', models.CharField(blank=True, default='', max_length=36, verbose_name='支付交易记录ID')),
                ('out_order_id', models.CharField(blank=True, default='', max_length=36, verbose_name='外部订单编号')),
                ('out_refund_id', models.CharField(blank=True, default='', max_length=64, verbose_name='外部退款单编号')),
                ('refund_reason', models.CharField(blank=True, default='', max_length=255, verbose_name='退款原因')),
                ('total_amounts', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='退款对应的交易订单总金额')),
                ('refund_amounts', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='申请退款金额')),
                ('real_refund', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='实际退款金额')),
                ('coupon_refund', models.DecimalField(decimal_places=2, default=Decimal('0'), help_text='资源券或者优惠抵扣金额，此金额不退', max_digits=10, verbose_name='资源券退款金额')),
                ('creation_time', models.DateTimeField(verbose_name='创建时间')),
                ('success_time', models.DateTimeField(default=None, null=True, verbose_name='退款成功时间')),
                ('status', models.CharField(choices=[('wait', '等待退款'), ('success', '退款成功'), ('error', '退款失败'), ('closed', '交易关闭')], default='wait', max_length=16, verbose_name='退款状态')),
                ('status_desc', models.CharField(default='', max_length=255, verbose_name='退款状态描述')),
                ('remark', models.CharField(default='', max_length=256, verbose_name='备注信息')),
                ('app_service_id', models.CharField(blank=True, default='', max_length=36, verbose_name='APP服务ID')),
                ('app_id', models.CharField(blank=True, default='', max_length=36, verbose_name='应用ID')),
                ('in_account', models.CharField(blank=True, default='', help_text='用户或VO余额ID, 及可能支持的其他账户', max_length=36, verbose_name='入账账户')),
                ('owner_id', models.CharField(blank=True, default='', help_text='user id or vo id', max_length=36, verbose_name='所属人ID')),
                ('owner_name', models.CharField(blank=True, default='', help_text='username or vo name', max_length=255, verbose_name='所属人名称')),
                ('owner_type', models.CharField(choices=[('user', '用户'), ('vo', 'VO组')], max_length=8, verbose_name='所属人类型')),
                ('operator', models.CharField(blank=True, default='', help_text='记录此次支付交易是谁执行完成的', max_length=128, verbose_name='交易操作人')),
            ],
            options={
                'verbose_name': '退款记录',
                'verbose_name_plural': '退款记录',
                'db_table': 'refund_record',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='TransactionBill',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(blank=True, default='', help_text='用户或VO余额ID, 及可能支持的其他账户', max_length=36, verbose_name='付款账户')),
                ('subject', models.CharField(default='', max_length=256, verbose_name='标题')),
                ('trade_type', models.CharField(choices=[('payment', '支付'), ('recharge', '充值'), ('refund', '退款')], max_length=16, verbose_name='交易类型')),
                ('trade_id', models.CharField(help_text='支付、退款、充值ID', max_length=36, verbose_name='交易id')),
                ('out_trade_no', models.CharField(default='', help_text='支付订单号、退款单号', max_length=64, verbose_name='外部交易编号')),
                ('trade_amounts', models.DecimalField(decimal_places=2, default=Decimal('0'), help_text='余额+券金额', max_digits=10, verbose_name='交易总金额')),
                ('amounts', models.DecimalField(decimal_places=2, help_text='16.66, -8.88', max_digits=10, verbose_name='金额')),
                ('coupon_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), help_text='资源券或者抵扣金额', max_digits=10, verbose_name='券金额')),
                ('after_balance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='交易后余额')),
                ('creation_time', models.DateTimeField(verbose_name='创建时间')),
                ('remark', models.CharField(blank=True, default='', max_length=255, verbose_name='备注信息')),
                ('owner_id', models.CharField(blank=True, default='', help_text='user id or vo id', max_length=36, verbose_name='所属人ID')),
                ('owner_name', models.CharField(blank=True, default='', help_text='username or vo name', max_length=255, verbose_name='所属人名称')),
                ('owner_type', models.CharField(choices=[('user', '用户'), ('vo', 'VO组')], max_length=8, verbose_name='所属人类型')),
                ('app_service_id', models.CharField(blank=True, default='', max_length=36, verbose_name='APP服务ID')),
                ('app_id', models.CharField(blank=True, default='', max_length=36, verbose_name='应用ID')),
                ('operator', models.CharField(blank=True, default='', help_text='记录此次支付交易是谁执行完成的', max_length=128, verbose_name='交易操作人')),
            ],
            options={
                'verbose_name': '交易流水账单',
                'verbose_name_plural': '交易流水账单',
                'db_table': 'transaction_bill',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='UserPointAccount',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default='0.00', max_digits=10, verbose_name='金额')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户账户',
                'verbose_name_plural': '用户账户',
                'db_table': 'user_point_account',
                'ordering': ['-creation_time'],
            },
        ),
        migrations.CreateModel(
            name='VoPointAccount',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default='0.00', max_digits=10, verbose_name='金额')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('vo', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vo.virtualorganization')),
            ],
            options={
                'verbose_name': 'VO组账户',
                'verbose_name_plural': 'VO组账户',
                'db_table': 'vo_point_account',
                'ordering': ['-creation_time'],
            },
        ),
    ]
