from django.utils.translation import gettext_lazy
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi

from api.viewsets import CustomGenericViewSet
from metering.models import PaymentStatus
from api.paginations import MeteringPageNumberPagination, StatementPageNumberPagination
from api.handlers.metering_handler import MeteringObsHandler, StorageStatementHandler
from api.serializers import serializers


class MeteringStorageViewSet(CustomGenericViewSet):
    permission_classes = [IsAuthenticated, ]
    pagination_class = MeteringPageNumberPagination
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary=gettext_lazy('列举对象存储用量计费账单'),
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
                name='bucket_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=gettext_lazy('查询指定存储桶')
            ),
            openapi.Parameter(
                name='date_start',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=gettext_lazy('计费账单日期起，默认当前月起始日期，ISO8601格式：YYYY-MM-dd')
            ),
            openapi.Parameter(
                name='date_end',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=gettext_lazy('计费账单日期止，默认当前月当前日期，ISO8601格式：YYYY-MM-dd')
            ),
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=gettext_lazy('查询指定用户的计费账单，仅以管理员身份查询时使用')
            ),
        ] + CustomGenericViewSet.PARAMETERS_AS_ADMIN + [
            openapi.Parameter(
                name='download',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                required=False,
                description=gettext_lazy('查询结果以文件方式下载文件；分页参数无效，不分页返回所有数据')
            ),
        ],
        responses={
            200: ''
        }
    )
    def list(self, request, *args, **kwargs):
        """
        列举对象存储用量计费账单

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
                  "daily_statement_id": "",
                  "service_id": "8d725d6a-30b5-11ec-a8e6-c8009fe2eb10",
                  "storage_bucket_id": "d24aa2fc-5d43-11ec-8f46-c8009fe2eb10",
                  "date": "2021-12-15",
                  "creation_time": "2022-04-02T09:14:07.754058Z",
                  "user_id": "1",
                  "username": "admin",
                  "storage": 45.64349609833334
                }
            }
        """
        return MeteringObsHandler().list_bucket_metering(view=self, request=request)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MeteringStorageSerializer

        return Serializer


class StatementStorageViewSet(CustomGenericViewSet):
    permission_classes = [IsAuthenticated, ]
    pagination_class = StatementPageNumberPagination
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary=gettext_lazy('列举日结算单'),
        request_body=no_body,
        manual_parameters=[
            openapi.Parameter(
                name='payment_status',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'支付状态，{PaymentStatus.choices}'
            ),
            openapi.Parameter(
                name='date_start',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'日结算单日期查询，时间段起，ISO8601格式：YYYY-MM-dd'
            ),
            openapi.Parameter(
                name='date_end',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description=f'日结算单日期查询，时间段止，ISO8601格式：YYYY-MM-dd'
            ),
        ],
        responses={
            200: ''
        }
    )
    def list(self, request, *args, **kwargs):
        """
        列举日结算单

            http code 200：
            {
              "count": 1,
              "page_num": 1,
              "page_size": 20,
              "statements": [
                {
                  "id": "s7649b7e624f211ed88b9c8009fe2eb44",
                  "original_amount": "16.32",
                  "payable_amount": "0.00",
                  "trade_amount": "0.00",
                  "payment_status": "unpaid",
                  "payment_history_id": "",
                  "date": "2022-01-01",
                  "creation_time": "2022-08-26T03:52:10.358606Z",
                  "user_id": "",
                  "username": "",
                  "service": {
                    "id": "1d35892c-36d3-11ec-8e3b-c8009fe2eb03",
                    "name": "iharbor",
                    "name_en": "iharbor",
                    "service_type": "iharbor"
                  }
                }
              ]
            }
        """
        return StorageStatementHandler().list_statement_storage(view=self, request=request)

    @swagger_auto_schema(
        operation_summary=gettext_lazy('日结算单详情'),
        request_body=no_body,
        responses={
            200: ''
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        日结算单详情

            http code 200：
            {
              "id": "s7647061824f211ed88b9c8009fe2eb44",
              "original_amount": "16.32",
              "payable_amount": "0.00",
              "trade_amount": "0.00",
              "payment_status": "unpaid",
              "payment_history_id": "",
              "date": "2022-01-01",
              "creation_time": "2022-08-26T03:52:10.341058Z",
              "user_id": "",
              "username": "",
              "service": {
               "id": "1d35892c-36d3-11ec-8e3b-c8009fe2eb03",
                    "name": "iharbor",
                    "name_en": "iharbor",
                    "service_type": "iharbor"
              }
            }
        """
        return StorageStatementHandler().statement_storage_detail(view=self, request=request, kwargs=kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DailyStatementStorageDetailSerializer
        elif self.action == 'retrieve':
            return serializers.DailyStatementStorageDetailSerializer

        return Serializer