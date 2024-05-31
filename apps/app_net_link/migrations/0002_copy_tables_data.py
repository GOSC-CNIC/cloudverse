# Generated by Django 4.2.9 on 2024-05-31 02:00

from django.db import migrations, connection, transaction

from apps.app_netbox.models import NetBoxUserRole
from apps.app_net_link.managers import NetLinkUserRoleWrapper


def run_copy_link(apps, schema_editor):
    with transaction.atomic():
        with connection.cursor() as cursor:
            # 光缆
            cursor.execute('INSERT INTO `net_link_fiber_cable`(`id`, `number`, `fiber_count`, `length`, `endpoint_1`, '
                           '`endpoint_2`, `remarks`, `create_time`, `update_time`) '
                           'SELECT `id`, `number`, `fiber_count`, `length`, `endpoint_1`, '
                           '`endpoint_2`, `remarks`, `create_time`, `update_time` FROM `netbox_fiber_cable`;')
            # 配线架, 外键机构二级
            cursor.execute('INSERT INTO `net_link_distribution_frame`(`id`, `number`, `model_type`, `row_count`, '
                           '`col_count`, `place`, `link_org_id`, `remarks`, `create_time`, `update_time`) '
                           'SELECT `id`, `number`, `model_type`, `row_count`, '
                           '`col_count`, `place`, `link_org_id`, `remarks`, `create_time`, `update_time` '
                           'FROM `netbox_distribution_frame`;')
            # 网元表
            cursor.execute('INSERT INTO `net_link_element`(`id`, `object_type`, `object_id`, `create_time`, `update_time`) '
                           'SELECT `id`, `object_type`, `object_id`, `create_time`, `update_time` FROM `netbox_element`;')
            # 租用线路，外键网元表
            cursor.execute('INSERT INTO `net_link_lease_line`('
                           '`id`, `element_id`, `private_line_number`, `lease_line_code`, `line_username`, `endpoint_a`,'
                           '`endpoint_z`, `line_type`, `cable_type`, `bandwidth`, `length`, `provider`, `enable_date`,'
                           '`is_whithdrawal`, `money`, `remarks`, `create_time`, `update_time`) '
                           'SELECT `id`, `element_id`, `private_line_number`, `lease_line_code`, `line_username`, `endpoint_a`,'
                           '`endpoint_z`, `line_type`, `cable_type`, `bandwidth`, `length`, `provider`, `enable_date`,'
                           '`is_whithdrawal`, `money`, `remarks`, `create_time`, `update_time` FROM `netbox_lease_line`;')
            # 光纤，外键 网元 光缆
            cursor.execute('INSERT INTO `net_link_optical_fiber`('
                           '`id`, `element_id`, `fiber_cable_id`, `sequence`, `create_time`, `update_time`) '
                           'SELECT `id`, `element_id`, `fiber_cable_id`, `sequence`, `create_time`, `update_time` '
                           'FROM `netbox_optical_fiber`;')
            # 配线架端口，外键 网元 配线架
            cursor.execute('INSERT INTO `net_link_distriframe_port`(`id`, `element_id`, `number`, `row`, `col`, '
                           '`distribution_frame_id`, `create_time`, `update_time`) '
                           'SELECT `id`, `element_id`, `number`, `row`, `col`, '
                           '`distribution_frame_id`, `create_time`, `update_time` FROM `netbox_distriframe_port`;')
            # 光缆接头盒，外键 网元
            cursor.execute('INSERT INTO `net_link_connector_box`(`id`, `element_id`, `number`, `place`, `remarks`, '
                           '`location`, `create_time`, `update_time`) '
                           'SELECT `id`, `element_id`, `number`, `place`, `remarks`, '
                           '`location`, `create_time`, `update_time` FROM `netbox_connector_box`;')
            # 链路表，多对多网元关系表
            cursor.execute('INSERT INTO `net_link_link`(`id`,`number`, `user`, `endpoint_a`, `endpoint_z`, `bandwidth`,'
                           '`description`, `line_type`, `business_person`, `build_person`, `create_time`, `update_time`,'
                           '`link_status`, `remarks`, `enable_date`) '
                           'SELECT `id`,`number`, `user`, `endpoint_a`, `endpoint_z`, `bandwidth`,'
                           '`description`, `line_type`, `business_person`, `build_person`, `create_time`, `update_time`,'
                           '`link_status`, `remarks`, `enable_date` FROM `netbox_link`;')
            cursor.execute('INSERT INTO `net_link_elementlink`(`id`, `element_id`, `link_id`, `index`, `sub_index`) '
                           'SELECT `id`, `element_id`, `link_id`, `index`, `sub_index` FROM `netbox_elementlink`;')

    print('[Ok] Copy 光缆、配线架、网元、租用线路、光纤、配线架端口、光缆接头盒、链路、链路网元关系 表数据 to app_net_link')


def reverse_copy_link(apps, schema_editor):
    with transaction.atomic(savepoint=False):
        with connection.cursor() as cursor:
            # 链路表，多对多网元关系表
            cursor.execute('DELETE FROM `net_link_elementlink`;')
            cursor.execute('DELETE FROM `net_link_link`;')
            # 光缆接头盒，外键 网元
            cursor.execute('TRUNCATE TABLE `net_link_connector_box`;')
            # 配线架端口，外键 网元 配线架
            cursor.execute('TRUNCATE TABLE `net_link_distriframe_port`;')
            # 光纤，外键 网元 光缆
            cursor.execute('TRUNCATE TABLE `net_link_optical_fiber`;')
            # 租用线路，外键网元表
            cursor.execute('TRUNCATE TABLE `net_link_lease_line`;')
            # 网元表
            cursor.execute('DELETE FROM `net_link_element`;')
            # 配线架, 外键机构二级
            cursor.execute('TRUNCATE TABLE `net_link_distribution_frame`;')
            # 光缆
            cursor.execute('TRUNCATE TABLE `net_link_fiber_cable`;')

    print('[Ok] Delete 光缆、配线架、网元、租用线路、光纤、配线架端口、光缆接头盒、链路、链路网元关系 表数据 from app_net_link')


def run_copy_net_link_user_role(apps, schema_editor):
    with transaction.atomic():
        for box_ur in NetBoxUserRole.objects.select_related('user').all():
            if box_ur.is_link_admin or box_ur.is_link_readonly:
                nlur = NetLinkUserRoleWrapper(box_ur.user)
                nlur.user_role = nlur.get_or_create_user_role()
                nlur.set_link_admin(box_ur.is_link_admin)
                nlur.set_link_readonly(box_ur.is_link_readonly)

    print('[Ok] Copy user role to app_net_link')


def reverse_copy_net_link_user_role(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM `net_link_user_role`;')

    print('[Ok] Delete user role from app_net_link')


class Migration(migrations.Migration):

    dependencies = [
        ('app_net_link', '0001_initial'),
    ]

    operations = [
        # 顺序要考虑到外键约束，run按正序执行，reverse按倒序执行
        migrations.RunPython(run_copy_net_link_user_role, reverse_code=reverse_copy_net_link_user_role),
        migrations.RunPython(run_copy_link, reverse_code=reverse_copy_link),
    ]