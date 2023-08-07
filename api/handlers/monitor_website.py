import time

from django.utils.translation import gettext as _
from rest_framework.response import Response

from core import errors
from monitor.managers import MonitorWebsiteManager, WebsiteQueryChoices
from monitor.models import MonitorWebsiteTask, MonitorWebsiteVersion, MonitorWebsite, WebsiteDetectionPoint
from api.viewsets import CustomGenericViewSet
from .handlers import serializer_error_msg


class MonitorWebsiteHandler:
    @staticmethod
    def create_website_task(view: CustomGenericViewSet, request):
        """
        创建一个站点监控任务
        """
        try:
            params = MonitorWebsiteHandler._create_website_validate_params(view=view, request=request)
            user = request.user
            if not user.is_federal_admin():
                count = MonitorWebsite.objects.filter(user_id=user.id).count()
                if count >= 2:
                    raise errors.ConflictError(message=_('已达到允许创建监控任务数量上限。'), code='TooManyTask')

            task = MonitorWebsiteManager.add_website_task(
                name=params['name'],
                scheme=params['scheme'],
                hostname=params['hostname'],
                uri=params['uri'],
                is_tamper_resistant=True if params['is_tamper_resistant'] else False,
                remark=params['remark'],
                user_id=request.user.id
            )
        except errors.Error as exc:
            return view.exception_response(exc)

        data = view.get_serializer(instance=task).data
        return Response(data=data)

    @staticmethod
    def _create_website_validate_params(view, request):
        """
        :raises: Error
        """
        serializer = view.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            s_errors = serializer.errors
            if 'name' in s_errors:
                exc = errors.BadRequest(message=_('无效的监控任务名称。') + s_errors['name'][0])
            elif 'scheme' in s_errors:
                exc = errors.BadRequest(
                    message=_('无效的站点协议。') + s_errors['scheme'][0], code='InvalidScheme')
            elif 'hostname' in s_errors:
                exc = errors.BadRequest(
                    message=_('无效的站点域名。') + s_errors['hostname'][0], code='InvalidHostname')
            elif 'uri' in s_errors:
                exc = errors.BadRequest(
                    message=_('无效的站点URI。') + s_errors['uri'][0], code='InvalidUri')
            elif 'remark' in s_errors:
                exc = errors.BadRequest(
                    message=_('问题相关的服务无效。') + s_errors['remark'][0])
            else:
                msg = serializer_error_msg(serializer.errors)
                exc = errors.BadRequest(message=msg)

            raise exc

        uri = serializer.validated_data.get('uri', '')
        if not uri or not uri.startswith('/'):
            raise errors.BadRequest(message=_('无效的站点URI，必须以“/”开头。'), code='InvalidUri')

        return serializer.validated_data

    @staticmethod
    def change_website_task(view: CustomGenericViewSet, request, kwargs):
        """
        修改站点监控信息任务
        """
        website_id = kwargs.get(view.lookup_field)
        try:
            params = MonitorWebsiteHandler._create_website_validate_params(view=view, request=request)
            task = MonitorWebsiteManager.change_website_task(
                _id=website_id,
                name=params['name'],
                scheme=params['scheme'],
                hostname=params['hostname'],
                uri=params['uri'],
                is_tamper_resistant=params['is_tamper_resistant'],
                remark=params['remark'],
                user=request.user
            )
        except errors.Error as exc:
            return view.exception_response(exc)

        data = view.get_serializer(instance=task).data
        return Response(data=data)

    @staticmethod
    def list_website_task(view: CustomGenericViewSet, request):
        """
        列举用户站点监控任务
        """
        try:
            queryset = MonitorWebsiteManager.get_user_website_queryset(user_id=request.user.id)
            websites = view.paginate_queryset(queryset=queryset)
        except Exception as exc:
            return view.exception_response(exc)

        data = view.get_serializer(instance=websites, many=True).data
        return view.get_paginated_response(data=data)

    @staticmethod
    def delete_website_task(view: CustomGenericViewSet, request, kwargs):
        """
        删除用户站点监控任务
        """
        try:
            website_id = kwargs.get(view.lookup_field)
            MonitorWebsiteManager.delete_website_task(_id=website_id, user=request.user)
        except Exception as exc:
            return view.exception_response(exc)

        return Response(status=204)

    @staticmethod
    def website_task_attention_mark(view: CustomGenericViewSet, request, kwargs):
        """
        站点监控任务特别关注标记
        """
        website_id = kwargs.get(view.lookup_field)
        action_ = request.query_params.get('action', '')
        action_ = action_.lower()
        if action_ == 'mark':
            is_attention = True
        elif action_ == 'unmark':
            is_attention = False
        else:
            return view.exception_response(
                exc=errors.InvalidArgument(message=_('操作参数的值无效，只允许选择“标记（mark）”和“取消标记（unmark）”。')))

        try:
            task = MonitorWebsiteManager.get_user_website(
                website_id=website_id,
                user=request.user
            )
            if task.is_attention != is_attention:
                task.is_attention = is_attention
                task.save(update_fields=['is_attention'])
        except errors.Error as exc:
            return view.exception_response(exc)

        data = view.get_serializer(instance=task).data
        return Response(data=data)

    @staticmethod
    def get_website_task_version(view: CustomGenericViewSet, request):
        ins = MonitorWebsiteVersion.get_instance()
        return Response(data={'version': ins.version})

    @staticmethod
    def monitor_list_website_task(view: CustomGenericViewSet, request):
        """
        拉取站点监控任务
        """
        try:
            queryset = MonitorWebsiteTask.objects.all()
            tasks = view.paginate_queryset(queryset=queryset)
        except Exception as exc:
            return view.exception_response(exc)

        data = view.get_serializer(instance=tasks, many=True).data
        return view.get_paginated_response(data=data)

    @staticmethod
    def query_monitor_data(view: CustomGenericViewSet, request, kwargs):
        """
        查询站点的监控数据
        """
        website_id = kwargs.get(view.lookup_field)
        query = request.query_params.get('query', None)
        detection_point_id = request.query_params.get('detection_point_id', None)

        if not detection_point_id:
            return view.exception_response(
                errors.BadRequest(message=_('必须指定探测点，参数“detection_ponit_id”是必须的')))

        if query is None:
            return view.exception_response(errors.BadRequest(message=_('参数"query"是必须提交的')))

        if query not in WebsiteQueryChoices.values:
            return view.exception_response(errors.InvalidArgument(message=_('参数"query"的值无效')))

        mgr = MonitorWebsiteManager()
        try:
            website = mgr.get_user_website(website_id=website_id, user=request.user)
        except errors.Error as exc:
            return view.exception_response(exc)

        try:
            data = mgr.query(website=website, tag=query, dp_id=detection_point_id)
        except errors.Error as exc:
            return view.exception_response(exc)

        return Response(data=data, status=200)

    @staticmethod
    def query_range_monitor_data(view: CustomGenericViewSet, request, kwargs):
        """
        查询站点的监控数据
        """
        website_id = kwargs.get(view.lookup_field)

        mgr = MonitorWebsiteManager()
        try:
            query, start, end, step, detection_point_id = MonitorWebsiteHandler.validate_query_range_params(request)
            website = mgr.get_user_website(website_id=website_id, user=request.user)
        except errors.Error as exc:
            return view.exception_response(exc)

        try:
            data = mgr.query_range(
                website=website, tag=query, start=start, end=end, step=step, dp_id=detection_point_id)
        except errors.Error as exc:
            return view.exception_response(exc)
        
        return Response(data=data, status=200)

    @staticmethod
    def validate_query_range_params(request):
        """
        :return:
            (service_id: str, query: str, start: int, end: int, step: int)

        :raises: Error
        """
        query = request.query_params.get('query', None)
        step = request.query_params.get('step', 300)
        detection_point_id = request.query_params.get('detection_point_id', None)

        if not detection_point_id:
            raise errors.BadRequest(message=_('必须指定探测点，参数“detection_ponit_id”是必须的'))

        if query is None:
            raise errors.BadRequest(message=_('参数"query"是必须提交的'))

        if query not in WebsiteQueryChoices.values:
            raise errors.InvalidArgument(message=_('参数"query"的值无效'))

        start, end = MonitorWebsiteHandler.validate_start_end_params(
            request=request, default_end=int(time.time()))

        timestamp_delta = end - start
        try:
            step = int(step)
        except ValueError:
            raise errors.InvalidArgument(message=_('步长"step"的值无效, 请尝试一个正整数'))

        if step <= 0:
            raise errors.InvalidArgument(message=_('不接受零或负查询解析步长, 请尝试一个正整数'))

        resolution = timestamp_delta // step
        if resolution > 10000:
            raise errors.BadRequest(message=_('超过了每个时间序列10000点的最大分辨率。尝试降低查询分辨率（？step=XX）'))

        return query, start, end, step, detection_point_id

    @staticmethod
    def list_website_detection_point(view: CustomGenericViewSet, request):
        """
        列举站点监控探测点
        """
        enable = request.query_params.get('enable', None)
        if isinstance(enable, str):
            enable = enable.lower()
            if enable == 'true':
                enable = True
            elif enable == 'false':
                enable = False
            else:
                return view.exception_response(errors.InvalidArgument('参数“enable”的值无效。'))

        queryset = WebsiteDetectionPoint.objects.all()
        if enable is not None:
            queryset = WebsiteDetectionPoint.objects.filter(enable=enable)

        try:
            points = view.paginate_queryset(queryset=queryset)
        except Exception as exc:
            return view.exception_response(exc)

        data = view.get_serializer(instance=points, many=True).data
        return view.get_paginated_response(data=data)

    @staticmethod
    def validate_start_end_params(request, default_start: int = None, default_end: int = None):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)

        if start:
            try:
                start = int(start)
                if start <= 0:
                    raise ValueError
            except ValueError:
                raise errors.InvalidArgument(message=_('起始时间"start"的值无效, 请尝试一个正整数'))
        else:
            if default_start:
                start = default_start
            else:
                raise errors.BadRequest(message=_('必须指定起始时间'))

        if end:
            try:
                end = int(end)
                if end <= 0:
                    raise ValueError
            except ValueError:
                raise errors.InvalidArgument(message=_('截止时间"end"的值无效, 请尝试一个正整数'))
        else:
            if default_end:
                end = default_end
            else:
                raise errors.BadRequest(message=_('必须指定截止时间'))

        timestamp_delta = end - start
        if timestamp_delta <= 0:
            raise errors.BadRequest(message=_('截止时间必须大于起始时间'))

        return start, end

    @staticmethod
    def list_duration_distribution(view: CustomGenericViewSet, request):
        now_st = int(time.time())
        start, end = MonitorWebsiteHandler.validate_start_end_params(
            request=request, default_start=now_st, default_end=now_st)
        detection_point_id = request.query_params.get('detection_point_id', None)

        mw_mgr = MonitorWebsiteManager()
        try:
            websites = mw_mgr.get_user_websites_qs(user=request.user)
            site_urls = [w.full_url for w in websites]
        except errors.Error as exc:
            return view.exception_response(exc)

        is_query_all = True if len(site_urls) > 10 else False

        if detection_point_id:
            point = mw_mgr.get_detection_ponit(dp_id=detection_point_id)
            detection_points = {detection_point_id: point}
        else:
            detection_points = mw_mgr.get_detection_ponits()

        dp_map_data = {}
        for dp in detection_points.values():
            try:
                if is_query_all:
                    res = mw_mgr.query_duration_avg(provider=dp.provider, start=start, end=end, site_urls=None)
                else:
                    res = mw_mgr.query_duration_avg(provider=dp.provider, start=start, end=end, site_urls=site_urls)
            except Exception as exc:
                res = []

            dp_map_data[dp.id] = res

        interval_map = {
            ">3s": (3,),
            "1s-3s": (1, 3),
            "600ms-1s": (0.6, 1),
            "300ms-600ms": (0.3, 0.6),
            "100ms-300ms": (0.1, 0.3),
            "50ms-100ms": (0.05, 0.1),
            "<50ms": (0, 0.05)
        }
        stat_map = {}
        for k, data in dp_map_data.items():
            r = MonitorWebsiteHandler._duration_interval_statistics(
                data=data, interval_map=interval_map, only_site_urls=site_urls)
            stat_map[k] = r

        return Response(data=stat_map)

    @staticmethod
    def _duration_interval_statistics(data: list, interval_map: dict, only_site_urls: list = None):
        """
        统计一个探针网站监控群的延迟分布情况
        如果指定 only_site_urls，只统计 only_site_urls 内的

        data:
        [
            {
                "metric": {
                    "job": "224e6e4a426968a95ae8c29c81155e1cc2911941",
                    "url": "https://yd.baidu.com/?pcf=2"
                },
                "value": [1690529936.783, "0.400814697"]
            },
        ]
        interval_map例如：
        {
            ">3s": (3,),
            "1s-3s": (1, 3),
            "50ms-1s": (0.05, 1),
            "<50ms": (0, 0.05)
        }

        :return:
        {
            ">3s": 1,
            "1s-3s": 3,
            "50ms-1s": 6,
            "<50ms": 0
        }
        """
        ret = {k: 0 for k in interval_map.keys()}  # 各区间初始值
        for item in data:
            value = float(item['value'][1])
            if only_site_urls and item['metric']['url'] not in only_site_urls:
                continue

            for k, v in interval_map.items():
                start, end = (v[0], None) if len(v) == 1 else (v[0], v[1])
                status = start < value if end is None else start <= value <= end
                if status is True:
                    ret[k] += 1
                    break

        return ret
