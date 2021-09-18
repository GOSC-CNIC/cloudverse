from django.utils.translation import gettext_lazy, gettext as _
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi

from servers.models import Server, Flavor
from servers.managers import ServerManager
from service.managers import ServiceManager
from service.models import DataCenter, ApplyOrganization, ApplyVmService
from service.models import ApplyQuota
from adapters import inputs, outputs
from core.quota import QuotaAPI
from core import request as core_request
from core import errors as exceptions
from core.taskqueue import server_build_status
from vo.models import VoMember
from activity.models import QuotaActivity
from api import serializers
from api.viewsets import CustomGenericViewSet
from api.paginations import DefaultPageNumberPagination
from api.handlers.service_quota_handler import ServiceQuotaHandler


class ServivePrivateQuotaViewSet(CustomGenericViewSet):
    """
    接入服务私有配额视图
    """
    permission_classes = [IsAuthenticated, ]
    pagination_class = DefaultPageNumberPagination
    lookup_field = 'id'
    # lookup_value_regex = '[0-9a-z-]+'

    @swagger_auto_schema(
        operation_summary=gettext_lazy('列举资源提供者接入服务的私有资源配额'),
        manual_parameters=[
            openapi.Parameter(
                name='service_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description='服务端点id'
            )
        ],
        responses={
            200: ''
        }
    )
    def list(self, request, *args, **kwargs):
        """
        列举资源提供者接入服务的私有资源配额

            http code 200：
            {
              "count": 1,
              "next": null,
              "previous": null,
              "results": [
                {
                  "private_ip_total": 0,
                  "public_ip_total": 0,
                  "vcpu_total": 0,
                  "ram_total": 0,
                  "disk_size_total": 0,
                  "private_ip_used": 0,
                  "public_ip_used": 0,
                  "vcpu_used": 0,
                  "ram_used": 0,
                  "disk_size_used": 0,
                  "creation_time": "2021-03-05T07:20:58.451119Z",
                  "enable": true,
                  "service": {
                    "id": "1",
                    "name": "地球大数据怀柔分中心"
                  }
                }
              ]
            }
        """
        return ServiceQuotaHandler.list_privete_quotas(view=self, request=request, kwargs=kwargs)


class ServiveShareQuotaViewSet(CustomGenericViewSet):
    """
    接入服务共享配额视图
    """
    permission_classes = [IsAuthenticated, ]
    pagination_class = DefaultPageNumberPagination
    lookup_field = 'id'
    # lookup_value_regex = '[0-9a-z-]+'

    @swagger_auto_schema(
        operation_summary=gettext_lazy('列举资源提供者接入服务的共享资源配额'),
        manual_parameters=[
            openapi.Parameter(
                name='service_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description='服务端点id'
            )
        ],
        responses={
            200: ''
        }
    )
    def list(self, request, *args, **kwargs):
        """
        列举资源提供者接入服务的共享资源配额

            http code 200：
            {
              "count": 1,
              "next": null,
              "previous": null,
              "results": [
                {
                  "private_ip_total": 0,
                  "public_ip_total": 0,
                  "vcpu_total": 0,
                  "ram_total": 0,
                  "disk_size_total": 0,
                  "private_ip_used": 0,
                  "public_ip_used": 0,
                  "vcpu_used": 0,
                  "ram_used": 0,
                  "disk_size_used": 0,
                  "creation_time": "2021-03-05T07:20:58.451119Z",
                  "enable": true,
                  "service": {
                    "id": "1",
                    "name": "地球大数据怀柔分中心"
                  }
                }
              ]
            }
        """
        return ServiceQuotaHandler.list_share_quotas(view=self, request=request, kwargs=kwargs)
