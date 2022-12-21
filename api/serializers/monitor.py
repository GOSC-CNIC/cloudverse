from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class MonitorJobCephSerializer(serializers.Serializer):
    id = serializers.CharField(label=_('监控单元id'))
    name = serializers.CharField(label=_('监控的CEPH集群名称'), max_length=255, default='')
    name_en = serializers.CharField(label=_('监控的CEPH集群英文名称'), max_length=255, default='')
    job_tag = serializers.CharField(label=_('CEPH集群标签名称'), max_length=255, default='')
    creation = serializers.DateTimeField(label=_('创建时间'))


class MonitorUnitCephSerializer(MonitorJobCephSerializer):
    """ceph监控单元"""
    remark = serializers.CharField(label=_('备注'))
    sort_weight = serializers.IntegerField(label=_('排序权重'), default=0, help_text=_('值越大排序越靠前'))
    grafana_url = serializers.CharField(label=_('Grafana连接'), max_length=255)
    dashboard_url = serializers.CharField(label=_('Dashboard连接'), max_length=255)


class MonitorJobServerSerializer(serializers.Serializer):
    id = serializers.CharField(label=_('监控单元id'))
    name = serializers.CharField(label=_('监控的主机集群'), max_length=255, default='')
    name_en = serializers.CharField(label=_('监控的主机集群英文名'), max_length=255, default='')
    job_tag = serializers.CharField(label=_('主机集群的标签名称'), max_length=255, default='')
    creation = serializers.DateTimeField(label=_('创建时间'))


class MonitorUnitServerSerializer(MonitorJobServerSerializer):
    """server监控单元"""
    remark = serializers.CharField(label=_('备注'))
    sort_weight = serializers.IntegerField(label=_('排序权重'), default=0, help_text=_('值越大排序越靠前'))
    grafana_url = serializers.CharField(label=_('Grafana连接'), max_length=255)
    dashboard_url = serializers.CharField(label=_('Dashboard连接'), max_length=255)


class MonitorJobVideoMeetingSerializer(serializers.Serializer):
    name = serializers.CharField(label=_('科技云会服务节点院所名称'), max_length=255, default='')
    name_en = serializers.CharField(label=_('科技云会服务节点院所英名称'), max_length=255, default='')
    job_tag = serializers.CharField(label=_('视频会议节点的标签名称'), max_length=255, default='')
    creation = serializers.DateTimeField(label=_('创建时间'))
    longitude = serializers.FloatField(label=_('经度'))
    latitude = serializers.FloatField(label=_('纬度'))