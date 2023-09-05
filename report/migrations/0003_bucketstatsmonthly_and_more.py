# Generated by Django 4.2.4 on 2023-09-04 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storage', '0002_initial'),
        ('report', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BucketStatsMonthly',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='ID')),
                ('bucket_id', models.CharField(max_length=36, verbose_name='存储桶ID')),
                ('bucket_name', models.CharField(max_length=73, verbose_name='存储桶名称')),
                ('size_byte', models.BigIntegerField(default=0, help_text='byte', verbose_name='存储容量(Byte)')),
                ('increment_byte', models.BigIntegerField(default=0, help_text='byte', verbose_name='存储容量增量(Byte)')),
                ('object_count', models.BigIntegerField(blank=True, default=0, verbose_name='桶对象数量')),
                ('original_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='计费金额')),
                ('increment_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='计费金额增量')),
                ('username', models.CharField(blank=True, default='', max_length=128, verbose_name='用户名')),
                ('date', models.DateField(help_text='根据数据采样周期，数据是哪个月的', verbose_name='数据日期(月份)')),
                ('creation_time', models.DateTimeField(verbose_name='创建时间')),
                ('service', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='storage.objectsservice', verbose_name='存储服务单元')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '存储桶月度容量增量统计数据',
                'verbose_name_plural': '存储桶月度容量增量统计数据',
                'db_table': 'bucket_stats_monthly',
                'ordering': ['-creation_time'],
                'indexes': [models.Index(fields=['date'], name='idx_date')],
            },
        ),
        migrations.AddConstraint(
            model_name='bucketstatsmonthly',
            constraint=models.UniqueConstraint(fields=('bucket_id', 'date'), name='unique_bucket_date'),
        ),
    ]
