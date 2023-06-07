import math
import io
from datetime import timedelta
from decimal import Decimal

from django.utils.http import urlquote
from django.utils import timezone
from django.http import StreamingHttpResponse
from django.utils.translation import gettext as _
from django.db.models import TextChoices
from rest_framework.response import Response

from users.managers import get_user_by_name
from core import errors
from api.viewsets import CustomGenericViewSet
from api.serializers.serializers import AdminCashCouponSerializer
from bill.managers import CashCouponManager
from bill.managers.cash_coupon import get_app_service_by_admin
from bill.models import CashCoupon, PayAppService, CashCouponPaymentHistory
from utils.report_file import CSVFileInMemory
from utils.time import iso_utc_to_datetime
from utils import rand_utils
from utils.decimal_utils import quantize_10_2
from .handlers import serializer_error_msg


class QueryCouponValidChoices(TextChoices):
    NOT_YET = 'notyet', '未起效'
    VALID = 'valid', '有效期内'
    EXPIRED = 'expired', '已过期'


class CashCouponHandler:
    def list_cash_coupon(self, view: CustomGenericViewSet, request):
        try:
            data = self.list_cash_coupon_validate_params(request=request)
        except errors.Error as exc:
            return view.exception_response(exc)

        vo_id = data['vo_id']
        valid = data['valid']
        app_service_id = data['app_service_id']
        app_service_category = data['app_service_category']

        mgr = CashCouponManager()
        if vo_id:
            queryset = mgr.get_vo_cash_coupon_queryset(
                user=request.user, vo_id=vo_id, valid=valid, app_service_id=app_service_id,
                app_service_category=app_service_category
            )
        else:
            queryset = mgr.get_user_cash_coupon_queryset(
                user_id=request.user.id, valid=valid, app_service_id=app_service_id,
                app_service_category=app_service_category
            )

        try:
            coupons = view.paginate_queryset(queryset)
            serializer = view.get_serializer(instance=coupons, many=True)
            return view.get_paginated_response(serializer.data)
        except Exception as exc:
            return view.exception_response(errors.convert_to_error(exc))

    @staticmethod
    def list_cash_coupon_validate_params(request):
        vo_id = request.query_params.get('vo_id', None)
        valid = request.query_params.get('valid', None)
        app_service_id = request.query_params.get('app_service_id', None)
        app_service_category = request.query_params.get('app_service_category', None)

        if vo_id == '':
            raise errors.BadRequest(message=_('参数“vo_id”值无效'), code='InvalidVoId')

        if app_service_category and app_service_category not in PayAppService.Category.values:
            raise errors.InvalidArgument(message=_('参数“app_service_category”值无效'), code='InvalidAppServiceCategory')

        if isinstance(valid, str):
            valid = valid.lower()
            if valid not in QueryCouponValidChoices.values:
                raise errors.InvalidArgument(message=_('参数“valid”值无效'), code='InvalidValid')
        else:
            valid = None

        return {
            'vo_id': vo_id,
            'valid': valid,
            'app_service_id': app_service_id,
            'app_service_category': app_service_category
        }

    def draw_cash_coupon(self, view: CustomGenericViewSet, request):
        try:
            coupon_id, coupon_code, vo_id = self.draw_cash_coupon_validate_params(request=request)
        except errors.Error as exc:
            return view.exception_response(exc)

        try:
            coupon = CashCouponManager().draw_cash_coupon(
                coupon_id=coupon_id, coupon_code=coupon_code, user=request.user, vo_id=vo_id
            )
        except Exception as exc:
            return view.exception_response(exc)

        return Response(data={'id': coupon.id})

    @staticmethod
    def draw_cash_coupon_validate_params(request) -> tuple:
        coupon_id = request.query_params.get('id', None)
        coupon_code = request.query_params.get('coupon_code', None)
        vo_id = request.query_params.get('vo_id', None)

        if coupon_id is None:
            raise errors.BadRequest(message=_('参数“id”必须指定'), code='MissingID')

        if not coupon_id:
            raise errors.BadRequest(message=_('参数“id”值无效'), code='InvalidID')

        if coupon_code is None:
            raise errors.BadRequest(message=_('参数“coupon_code”必须指定'), code='MissingCouponCode')

        if not coupon_code:
            raise errors.BadRequest(message=_('参数“coupon_code”值无效'), code='InvalidCouponCode')

        if vo_id is not None and not vo_id:
            raise errors.BadRequest(message=_('参数“vo_id”值无效'), code='InvalidVoId')

        return coupon_id, coupon_code, vo_id

    @staticmethod
    def delete_cash_coupon(view: CustomGenericViewSet, request, kwargs):
        coupon_id = kwargs.get(view.lookup_field, None)
        force = request.query_params.get('force', None)
        force = force is not None

        try:
            CashCouponManager().delete_cash_coupon(coupon_id=coupon_id, user=request.user, force=force)
        except Exception as exc:
            return view.exception_response(exc)

        return Response(status=204)

    @staticmethod
    def list_cash_coupon_payment(view: CustomGenericViewSet, request, kwargs):
        """
        列举券支付记录
        """
        coupon_id = kwargs.get(view.lookup_field)
        try:
            queryset = CashCouponManager().get_cash_coupon_payment_queryset(coupon_id=coupon_id, user=request.user)
        except Exception as exc:
            return view.exception_response(exc)

        try:
            coupons = view.paginate_queryset(queryset)
            serializer = view.get_serializer(instance=coupons, many=True)
            return view.get_paginated_response(serializer.data)
        except Exception as exc:
            return view.exception_response(errors.convert_to_error(exc))

    def admin_list_cash_coupon(self, view: CustomGenericViewSet, request):
        try:
            data = self._admin_list_cash_coupon_validate_params(request=request)
        except errors.Error as exc:
            return view.exception_response(exc)

        template_id = data['template_id']
        status = data['status']
        app_service_id = data['app_service_id']
        valid = data['valid']
        redeemer = data['redeemer']
        issuer = data['issuer']
        download = data['download']
        time_start = data['time_start']
        time_end = data['time_end']

        try:
            queryset = CashCouponManager().admin_list_coupon_queryset(
                user=request.user, template_id=template_id, app_service_id=app_service_id, status=status, valid=valid,
                issuer=issuer, redeemer=redeemer, createtime_start=time_start, createtime_end=time_end
            )

            if download:
                return self.admin_list_coupon_download(queryset=queryset)

            coupons = view.paginate_queryset(queryset)
            serializer = view.get_serializer(instance=coupons, many=True)
            return view.get_paginated_response(serializer.data)
        except Exception as exc:
            return view.exception_response(errors.convert_to_error(exc))

    @staticmethod
    def _admin_list_cash_coupon_validate_params(request):
        template_id = request.query_params.get('template_id', None)
        status = request.query_params.get('status', None)
        app_service_id = request.query_params.get('app_service_id', None)
        valid_status = request.query_params.get('valid_status', None)
        redeemer = request.query_params.get('redeemer', None)
        issuer = request.query_params.get('issuer', None)
        download = request.query_params.get('download', None)
        time_start = request.query_params.get('time_start', None)
        time_end = request.query_params.get('time_end', None)

        if issuer is not None and not issuer:
            raise errors.InvalidArgument(message=_('指定的发放人不能为空'))

        if redeemer is not None and not redeemer:
            raise errors.InvalidArgument(message=_('指定的兑换人不能为空'))

        if status and status not in CashCoupon.Status.values:
            raise errors.InvalidArgument(message=_('参数“status”的值无效'))

        if isinstance(valid_status, str):
            valid = valid_status.lower()
            if valid not in QueryCouponValidChoices.values:
                raise errors.InvalidArgument(message=_('参数“valid”值无效'), code='InvalidValid')
        else:
            valid = None

        if time_start is not None:
            time_start = iso_utc_to_datetime(time_start)
            if time_start is None:
                raise errors.InvalidArgument(message=_('参数“time_start”的值无效的时间格式'))

        if time_end is not None:
            time_end = iso_utc_to_datetime(time_end)
            if time_end is None:
                raise errors.InvalidArgument(message=_('参数“time_end”的值无效的时间格式'))

        if time_start and time_end:
            if time_start >= time_end:
                raise errors.InvalidArgument(message=_('参数“time_start”时间必须超前“time_end”时间'))

        return {
            'template_id': template_id,
            'status': status,
            'valid': valid,
            'app_service_id': app_service_id,
            'issuer': issuer,
            'redeemer': redeemer,
            'download': download is not None,
            'time_start': time_start,
            'time_end': time_end
        }

    def admin_list_coupon_download(self, queryset):
        count = queryset.count()
        if count > 100000:
            exc = errors.ConflictError(message=_('数据量太多'), code='TooManyData')
            return Response(data=exc.err_data(), status=exc.status_code)

        filename = rand_utils.timestamp14_sn()
        csv_file = CSVFileInMemory(filename=filename)
        csv_file.writerow(['#' + _('代金券明细')])
        csv_file.writerow(['#--------------' + _('数据明细列表') + '---------------'])
        csv_file.writerow([
            _('代金券编号'), _('面额'), _('余额'), _('服务单元'), _('创建日期'), _('生效日期'), _('过期时间'),
            _('状态'), _('券模板'), _('兑换码'), _('所有者类型'), _('用户'), _('VO组名')
        ])
        per_page = 1000
        is_end_page = False
        for number in range(1, math.ceil(count / per_page) + 1):
            bottom = (number - 1) * per_page
            top = bottom + per_page
            if top >= count:
                top = count
                is_end_page = True

            coupons = queryset[bottom:top]
            rows = []
            for c in coupons:
                c: CashCoupon
                app_service_name = c.app_service.name if c.app_service else "空"
                tpl_name = c.activity.name if c.activity else "空"
                username = c.user.username if c.user else '空'
                voname = c.vo.name if c.vo else '空'

                line_items = [
                    str(c.id), str(quantize_10_2(c.face_value)), str(quantize_10_2(c.balance)),
                    str(app_service_name), c.creation_time.isoformat(), c.effective_time.isoformat(),
                    c.expiration_time.isoformat(), str(c.get_status_display()),
                    tpl_name, c.one_exchange_code, str(c.owner_type), username, voname
                ]
                rows.append(line_items)

            csv_file.writerows(rows)
            if is_end_page:
                break

        csv_file.writerow(['#--------------' + _('数据明细列表结束') + '---------------'])
        csv_file.writerow(['#' + _('数据总数') + f': {count}'])
        csv_file.writerow(['#' + _('下载时间') + f': {timezone.now()}'])

        filename = csv_file.filename
        data = csv_file.to_bytes()
        csv_file.close()
        return self._wrap_csv_file_response(filename=filename, data=data)

    @staticmethod
    def _wrap_csv_file_response(filename: str, data):
        """
        :param data: bytes, BytesIO， StringIO
        """
        if isinstance(data, bytes):
            content_type = 'application/octet-stream'
            content_length = len(data)
            data = io.BytesIO(data)
        elif isinstance(data, io.StringIO):
            content_type = 'text/csv'
            content_length = None
            data.seek(0)
        else:
            content_type = 'application/octet-stream'
            content_length = data.seek(0, io.SEEK_END)
            data.seek(0)

        filename = urlquote(filename)  # 中文文件名需要
        response = StreamingHttpResponse(data, charset='utf-8', status=200)
        if content_length:
            response['Content-Length'] = content_length  # byte length

        response['Content-Type'] = content_type
        response['Content-Disposition'] = f"attachment;filename*=utf-8''{filename}"  # 注意filename 这个是下载后的名字
        return response

    def exchange_cash_coupon(self, view: CustomGenericViewSet, request):
        """兑换码兑换代金券"""
        try:
            code, vo_id = self._exchange_cash_coupon_validate_params(request=request)
        except errors.Error as exc:
            return view.exception_response(exc)

        coupon_id, coupon_code = CashCoupon.parse_exchange_code(code=code)

        try:
            coupon = CashCouponManager().draw_cash_coupon(
                coupon_id=coupon_id, coupon_code=coupon_code, user=request.user, vo_id=vo_id
            )
        except Exception as exc:
            return view.exception_response(exc)

        return Response(data={'id': coupon.id})

    @staticmethod
    def _exchange_cash_coupon_validate_params(request) -> tuple:
        code = request.query_params.get('code', None)
        vo_id = request.query_params.get('vo_id', None)

        if code is None:
            raise errors.BadRequest(message=_('参数“code”必须指定'), code='MissingCode')

        if not code:
            raise errors.BadRequest(message=_('参数“code”值无效'), code='InvalidCode')

        if len(code) < 10:
            raise errors.BadRequest(message=_('参数“code”值无效'), code='InvalidCode')

        if vo_id is not None and not vo_id:
            raise errors.BadRequest(message=_('参数“vo_id”值无效'), code='InvalidVoId')

        return code, vo_id

    @staticmethod
    def admin_create_cash_coupon(view: CustomGenericViewSet, request):
        """
        App服务单元管理员创建一个代金券，可直接发放给指定用户
        """
        try:
            data = CashCouponHandler._admin_create_cash_coupon_validate_params(view=view, request=request)
        except errors.Error as exc:
            return view.exception_response(exc)

        face_value = data['face_value']
        effective_time = data['effective_time']
        expiration_time = data['expiration_time']
        app_service = data['app_service']
        user = data['user']

        try:
            if user is None:
                coupon, coupon_num = CashCouponManager().create_wait_draw_coupon(
                    app_service_id=app_service.id,
                    face_value=face_value,
                    effective_time=effective_time,
                    expiration_time=expiration_time,
                    coupon_num=0,
                    issuer=request.user.username
                )
            else:
                coupon = CashCouponManager().create_one_coupon_to_user(
                    user=user,
                    app_service_id=app_service.id,
                    face_value=face_value,
                    effective_time=effective_time,
                    expiration_time=expiration_time,
                    issuer=request.user.username
                )
        except Exception as exc:
            return view.exception_response(exc)

        return Response(data=AdminCashCouponSerializer(instance=coupon).data)

    @staticmethod
    def _admin_create_cash_coupon_validate_params(view: CustomGenericViewSet, request):
        serializer = view.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            s_errors = serializer.errors
            if 'face_value' in s_errors:
                exc = errors.BadRequest(
                    message=_('代金券面额无效。') + s_errors['face_value'][0], code='InvalidFaceValue')
            elif 'effective_time' in s_errors:
                exc = errors.BadRequest(
                    message=_('代金券生效时间无效。') + s_errors['effective_time'][0], code='InvalidEffectiveTime')
            elif 'expiration_time' in s_errors:
                exc = errors.BadRequest(
                    message=_('代金券过期时间无效。') + s_errors['expiration_time'][0], code='InvalidExpirationTime')
            else:
                msg = serializer_error_msg(serializer.errors)
                exc = errors.BadRequest(message=msg)

            raise exc

        data = serializer.validated_data
        face_value = data['face_value']
        effective_time = data['effective_time']
        expiration_time = data['expiration_time']
        app_service_id = data['app_service_id']
        username = data.get('username', None)

        if face_value < 0 or face_value > 100000:
            raise errors.BadRequest(message=_('代金券面额必须大于0，不得大于100000'), code='InvalidFaceValue')

        now_time = timezone.now()
        if (expiration_time - now_time) < timedelta(hours=1):
            raise errors.BadRequest(message=_('代金券的过期时间与当前时间的时间差必须大于1小时'), code='InvalidExpirationTime')

        if effective_time:
            if (expiration_time - effective_time) < timedelta(hours=1):
                raise errors.BadRequest(
                    message=_('代金券的过期时间与生效时间的时间差必须大于1小时'), code='InvalidExpirationTime')
        else:
            effective_time = now_time

        # AppServiceNotExist, AccessDenied
        app_service = get_app_service_by_admin(_id=app_service_id, user=request.user)

        if username:
            user = get_user_by_name(username=username)      # UserNotExist
        else:
            user = None

        return {
            'face_value': face_value,
            'effective_time': effective_time,
            'expiration_time': expiration_time,
            'app_service': app_service,
            'user': user
        }

    @staticmethod
    def detail_cash_coupon(view: CustomGenericViewSet, request, kwargs):
        """
        查询代金券详情
        """
        coupon_id = kwargs.get(view.lookup_field)

        ccmgr = CashCouponManager()
        try:
            coupon = ccmgr.get_cash_coupon(
                coupon_id=coupon_id, select_for_update=False,
                related_fields=['vo', 'user', 'activity', 'app_service']
            )
            ccmgr.has_read_perm_cash_coupon(coupon=coupon, user=request.user)
            serializer = view.get_serializer(instance=coupon)
            return Response(data=serializer.data)
        except Exception as exc:
            return view.exception_response(exc)

    @staticmethod
    def admin_detail_cash_coupon(view: CustomGenericViewSet, request, kwargs):
        """
        管理员查询代金券详情
        """
        coupon_id = kwargs.get(view.lookup_field)

        ccmgr = CashCouponManager()
        try:
            coupon = ccmgr.get_cash_coupon(
                coupon_id=coupon_id, select_for_update=False,
                related_fields=['vo', 'user', 'activity', 'app_service']
            )
            ccmgr.has_admin_perm_cash_coupon(coupon=coupon, user=request.user)
            serializer = view.get_serializer(instance=coupon)
            return Response(data=serializer.data)
        except Exception as exc:
            return view.exception_response(exc)

    @staticmethod
    def admin_delete_cash_coupon(view: CustomGenericViewSet, request, kwargs):
        coupon_id = kwargs.get(view.lookup_field, None)

        try:
            CashCouponManager().admin_delete_cash_coupon(coupon_id=coupon_id, user=request.user)
        except Exception as exc:
            return view.exception_response(exc)

        return Response(status=204)

    @staticmethod
    def admin_list_cash_coupon_payment(view: CustomGenericViewSet, request, kwargs):
        """
        列举券支付记录
        """
        coupon_id = kwargs.get(view.lookup_field)
        try:
            queryset = CashCouponManager().admin_get_cash_coupon_payment_queryset(
                coupon_id=coupon_id, user=request.user)
        except Exception as exc:
            return view.exception_response(exc)

        try:
            coupons = view.paginate_queryset(queryset)
            serializer = view.get_serializer(instance=coupons, many=True)
            return view.get_paginated_response(serializer.data)
        except Exception as exc:
            return view.exception_response(errors.convert_to_error(exc))

    @staticmethod
    def admin_cash_coupon_statistics(view: CustomGenericViewSet, request, kwargs):
        """
        联邦管理员查询券统计信息
        """
        from django.db.models import Count, Sum

        time_start = request.query_params.get('time_start', None)
        time_end = request.query_params.get('time_end', None)
        app_service_id = request.query_params.get('app_service_id', None)

        try:
            if time_start is not None:
                time_start = iso_utc_to_datetime(time_start)
                if time_start is None:
                    raise errors.InvalidArgument(message=_('参数“time_start”的值无效的时间格式'))

            if time_end is not None:
                time_end = iso_utc_to_datetime(time_end)
                if time_end is None:
                    raise errors.InvalidArgument(message=_('参数“time_end”的值无效的时间格式'))

            if time_start and time_end:
                if time_start >= time_end:
                    raise errors.InvalidArgument(message=_('参数“time_start”时间必须超前“time_end”时间'))
        except Exception as exc:
            return view.exception_response(exc)

        try:
            if not request.user.is_federal_admin():
                raise errors.AccessDenied(message=_('你没有联邦管理员权限。'))

            lookups = {}
            if time_start:
                lookups['creation_time__gte'] = time_start
            if time_end:
                lookups['creation_time__lte'] = time_end
            if app_service_id:
                lookups['app_service_id'] = app_service_id

            r = CashCoupon.objects.filter(**lookups).aggregate(
                total_count=Count('id', distinct=True),
                total_face_value=Sum('face_value')
            )
            total_count = r['total_count']
            total_face_value = r['total_face_value'] if r['total_face_value'] else Decimal(0.00)

            # 兑换券数量
            redeem_count = CashCoupon.objects.filter(**lookups).exclude(status=CashCoupon.Status.WAIT.value).count()

            # 券总消费点数，时间段参数无效
            lookups = {}
            if app_service_id:
                lookups['cash_coupon__app_service_id'] = app_service_id
            r = CashCouponPaymentHistory.objects.filter(**lookups).aggregate(
                coupon_pay_amounts=Sum('amounts'))
            coupon_pay_amounts = r['coupon_pay_amounts'] if r['coupon_pay_amounts'] else Decimal('0.00')
            coupon_pay_amounts = -coupon_pay_amounts

            # 有效券总余额，时间段参数无效
            lookups = {}
            if app_service_id:
                lookups['app_service_id'] = app_service_id
            r = CashCoupon.objects.filter(
                **lookups, expiration_time__gt=timezone.now(),
                status=CashCoupon.Status.AVAILABLE.value
            ).aggregate(total_balance=Sum('balance'))
            total_balance = r['total_balance'] if r['total_balance'] else Decimal('0.00')
        except Exception as exc:
            return view.exception_response(exc)

        return Response(data={
            'total_face_value': total_face_value,
            'total_count': total_count,
            'redeem_count': redeem_count,
            'coupon_pay_amounts': coupon_pay_amounts,
            'total_balance': total_balance
        })
