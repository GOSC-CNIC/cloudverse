from django.utils.translation import gettext_lazy
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi

from api.viewsets import CustomGenericViewSet
from api.paginations import MeteringPageNumberPagination
from api.handlers.metering_handler import MeteringHandler
from api import serializers


class MeteringServerViewSet(CustomGenericViewSet):

    permission_classes = [IsAuthenticated, ]
    pagination_class = MeteringPageNumberPagination
    lookup_field = 'id'
    # lookup_value_regex = '[0-9a-z-]+'

    @swagger_auto_schema(
        operation_summary=gettext_lazy('列举云主机用量计费账单'),
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter(
                name='service_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'查询指定服务'
            ),
            openapi.Parameter(
                name='server_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'查询指定云主机'
            ),
            openapi.Parameter(
                name='date_start',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'计费账单日期起，默认当前月起始日期，ISO8601格式：YYYY-MM-dd'
            ),
            openapi.Parameter(
                name='date_end',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'计费账单日期止，默认当前月当前日期，ISO8601格式：YYYY-MM-dd'
            ),
            openapi.Parameter(
                name='vo_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'查询指定VO组的计费账单，需要vo组权限, 或管理员权限，不能与user_id同时使用'
            ),
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'查询指定用户的计费账单，仅以管理员身份查询时使用'
            ),
        ] + CustomGenericViewSet.PARAMETERS_AS_ADMIN,
        responses={
            200: ''
        }
    )
    def list(self, request, *args, **kwargs):
        """
        列举云主机用量计费账单

            http code 200：
            {
              "count": 1,
              "page_num": 1,
              "page_size": 20,
              "results": [
                {
                  "id": "400ad412-b265-11ec-9dad-c8009fe2eb10",
                  "original_amount": "2.86",
                  "trade_amount": "0.00",
                  "payment_status": "unpaid",
                  "payment_history_id": null,
                  "service_id": "8d725d6a-30b5-11ec-a8e6-c8009fe2eb10",
                  "server_id": "d24aa2fc-5d43-11ec-8f46-c8009fe2eb10",
                  "date": "2021-12-15",
                  "creation_time": "2022-04-02T09:14:07.754058Z",
                  "user_id": "1",
                  "vo_id": "",
                  "owner_type": "user",
                  "cpu_hours": 45.64349609833334,
                  "ram_hours": 91.28699219666667,
                  "disk_hours": 0,
                  "public_ip_hours": 22.82174804916667,
                  "snapshot_hours": 0,
                  "upstream": 0,
                  "downstream": 0,
                  "pay_type": "postpaid"
                }
            }
        """
        return MeteringHandler().list_server_metering(view=self, request=request)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MeteringServerSerializer

        return serializers.serializers.Serializer