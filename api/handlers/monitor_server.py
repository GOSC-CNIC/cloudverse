import time
from django.utils.translation import gettext, gettext_lazy as _
from rest_framework.response import Response

from core import errors
from monitor.managers import MonitorJobServerManager, ServerQueryChoices


class MonitorServerQueryHandler:
    def query(self, view, request, kwargs):
        query = request.query_params.get('query', None)
        service_id = request.query_params.get('service_id', None)

        if query is None:
            return view.exception_response(errors.BadRequest(message=_('参数"query"是必须提交的')))

        if query not in ServerQueryChoices.values:
            return view.exception_response(errors.InvalidArgument(message=_('参数"query"的值无效')))

        if service_id is None:
            return view.exception_response(errors.BadRequest(message=_('参数"service_id"是必须提交的')))

        try:
            self.check_permission(view=view, service_id=service_id, user=request.user)
        except errors.Error as exc:
            return view.exception_response(exc)

        try:
            data = MonitorJobServerManager().query(tag=query, service_id=service_id)
        except errors.Error as exc:
            return view.exception_response(exc)

        return Response(data=data, status=200)

    @staticmethod
    def check_permission(view, service_id: str, user):
        """
        :return:
            service
        :raises: Error
        """
        try:
            service = view.get_service_by_id(service_id)
        except errors.Error as exc:
            raise exc

        if user.is_federal_admin() or service.user_has_perm(user):     # 服务管理员权限
            return service

        raise errors.AccessDenied(message=gettext('你没有指定服务的管理权限'))