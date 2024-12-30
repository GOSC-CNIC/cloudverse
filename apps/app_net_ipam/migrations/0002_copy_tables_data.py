# Generated by Django 4.2.9 on 2024-05-31 06:23

from django.db import migrations, connection, transaction

from apps.app_net_ipam.managers import NetIPamUserRoleWrapper
from apps.app_users.models import UserProfile
# from apps.app_netbox.models import NetBoxUserRole


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def run_copy_asn_ipv4v6range(apps, schema_editor):
    with transaction.atomic():
        with connection.cursor() as cursor:
            # 复制asn
            cursor.execute('INSERT INTO `net_ipam_asn`(`id`, `number`, `name`, `creation_time`) '
                           'SELECT `id`, `number`, `name`, `creation_time` FROM `netbox_asn`;')
            # ipv4range ipv4
            cursor.execute('INSERT INTO `net_ipam_ipv4_range`(`id`, `name`, `status`, `creation_time`, `update_time`,'
                           '`assigned_time`, `asn_id`, `admin_remark`, `remark`, `org_virt_obj_id`, `start_address`,'
                           '`end_address`, `mask_len`) '
                           'SELECT `id`, `name`, `status`, `creation_time`, `update_time`,'
                           '`assigned_time`, `asn_id`, `admin_remark`, `remark`, `org_virt_obj_id`, `start_address`,'
                           '`end_address`, `mask_len` FROM `netbox_ipv4_range`;')
            cursor.execute('INSERT INTO `net_ipam_ipv4_addr`('
                           '`id`, `creation_time`, `update_time`, `admin_remark`, `remark`, `ip_address`) '
                           'SELECT `id`, `creation_time`, `update_time`, `admin_remark`, `remark`, `ip_address` '
                           'FROM `netbox_ipv4_addr`;')
            cursor.execute('INSERT INTO `net_ipam_ipv4_range_record`('
                           '`id`, `creation_time`, `record_type`, `ip_ranges`, `remark`, `user_id`, `org_virt_obj_id`,'
                           '`start_address`, `end_address`, `mask_len`) '
                           'SELECT `id`, `creation_time`, `record_type`, `ip_ranges`, `remark`, `user_id`, `org_virt_obj_id`,'
                           '`start_address`, `end_address`, `mask_len` FROM `netbox_ipv4_range_record`;')
            # ipv6range ipv6
            cursor.execute('INSERT INTO `net_ipam_ipv6_range`(`id`, `name`, `status`, `creation_time`, `update_time`,'
                           '`assigned_time`, `asn_id`, `admin_remark`, `remark`, `org_virt_obj_id`, `start_address`,'
                           '`end_address`, `prefixlen`) '
                           'SELECT `id`, `name`, `status`, `creation_time`, `update_time`,'
                           '`assigned_time`, `asn_id`, `admin_remark`, `remark`, `org_virt_obj_id`, `start_address`,'
                           '`end_address`, `prefixlen` FROM `netbox_ipv6_range`;')
            cursor.execute('INSERT INTO `net_ipam_ipv6_addr`('
                           '`id`, `creation_time`, `update_time`, `admin_remark`, `remark`, `ip_address`) '
                           'SELECT `id`, `creation_time`, `update_time`, `admin_remark`, `remark`, `ip_address` '
                           'FROM `netbox_ipv6_addr`;')
            cursor.execute('INSERT INTO `net_ipam_ipv6_range_record`('
                           '`id`, `creation_time`, `record_type`, `ip_ranges`, `remark`, `user_id`, `org_virt_obj_id`,'
                           '`start_address`, `end_address`, `prefixlen`) '
                           'SELECT `id`, `creation_time`, `record_type`, `ip_ranges`, `remark`, `user_id`, `org_virt_obj_id`,'
                           '`start_address`, `end_address`, `prefixlen` FROM `netbox_ipv6_range_record`;')

    print('[Ok] Copy ASN、IPv4/6Range、Record and Address to app_net_ipam')


def reverse_copy_asn_ipv4v6range(apps, schema_editor):
    with transaction.atomic(savepoint=False):
        with connection.cursor() as cursor:
            # ipv4
            cursor.execute('TRUNCATE TABLE `net_ipam_ipv4_addr`;')
            cursor.execute('TRUNCATE TABLE `net_ipam_ipv4_range_record`;')
            cursor.execute('TRUNCATE TABLE `net_ipam_ipv4_range`;')

            # ipv6
            cursor.execute('TRUNCATE TABLE `net_ipam_ipv6_addr`;')
            cursor.execute('TRUNCATE TABLE `net_ipam_ipv6_range_record`;')
            cursor.execute('TRUNCATE TABLE `net_ipam_ipv6_range`;')

            # ASN
            # cursor.execute('TRUNCATE TABLE `net_ipam_asn`;')    # TRUNCATE会受外键约束限制
            cursor.execute('DELETE FROM `net_ipam_asn`;')

    print('[Ok] Delete ASN、IPv4/6Range、Record and Address from app_net_ipam')


def run_copy_net_ipam_user_role(apps, schema_editor):
    with transaction.atomic():
        # for box_ur in NetBoxUserRole.objects.select_related('user').all():
        #     if box_ur.is_ipam_admin or box_ur.is_ipam_readonly:
        #         nlur = NetIPamUserRoleWrapper(box_ur.user)
        #         nlur.user_role = nlur.get_or_create_user_role()
        #         nlur.set_ipam_admin(box_ur.is_ipam_admin)
        #         nlur.set_ipam_readonly(box_ur.is_ipam_readonly)

        cursor = connection.cursor()
        sql = 'SELECT `t1`.`id`, `t1`.`user_id`, `t1`.`is_ipam_admin`, `t1`.`is_ipam_readonly` FROM `netbox_user_role` AS `t1`'
        cursor.execute(sql)
        objs = dictfetchall(cursor)
        for box_ur in objs:
            is_ipam_admin = box_ur['is_ipam_admin']
            is_ipam_readonly = box_ur['is_ipam_readonly']
            if is_ipam_admin or is_ipam_readonly:
                user = UserProfile.objects.filter(id=box_ur['user_id']).first()
                if not user:
                    continue

                nlur = NetIPamUserRoleWrapper(user)
                nlur.user_role = nlur.get_or_create_user_role()
                nlur.set_ipam_admin(is_ipam_admin)
                nlur.set_ipam_readonly(is_ipam_readonly)

    print('[Ok] Copy user role to app_net_ipam')


def reverse_copy_net_link_user_role(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM `net_ipam_user_role`;')

    print('[Ok] Delete user role from app_net_ipam')


class Migration(migrations.Migration):

    dependencies = [
        ('app_net_ipam', '0001_initial'),
    ]

    operations = [
        # migrations.RunPython(run_copy_net_ipam_user_role, reverse_code=reverse_copy_net_link_user_role),
        # migrations.RunPython(run_copy_asn_ipv4v6range, reverse_code=reverse_copy_asn_ipv4v6range),
    ]
