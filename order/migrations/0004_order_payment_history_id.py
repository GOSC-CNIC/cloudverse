# Generated by Django 3.2.13 on 2022-07-05 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20220624_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_history_id',
            field=models.CharField(blank=True, default='', max_length=36, verbose_name='支付记录id'),
        ),
    ]