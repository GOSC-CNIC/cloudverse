import time
from urllib import parse

import requests
import aiohttp
from string import Template

from core import errors
from monitor.utils import ThanosProvider


class ExpressionQuery:
    server_health_status = 'count(node_uname_info{job="$job"}) - count(up{job="$job"} == 1)'
    server_host_up_count = 'count(up{job="$job"} == 1)'
    server_host_count = 'count(node_uname_info{job="$job"})'
    server_cpu_usage = 'avg(1 - avg(rate(node_cpu_seconds_total{job="$job",mode="idle"}[30s])) by (instance))*100'
    server_mem_usage = 'avg((1 - (node_memory_MemAvailable_bytes{job="$job"} / ' \
                       '(node_memory_MemTotal_bytes{job="$job"} - node_memory_HugePages_Total{job="$job"} * ' \
                       'node_memory_Hugepagesize_bytes{job="$job"})))* 100)'
    server_disk_usage = 'avg((node_filesystem_size_bytes{job="$job",fstype=~"ext.?|xfs"}'\
                        '-node_filesystem_free_bytes{job="$job",fstype=~"ext.?|xfs"}) *100'\
                        '/(node_filesystem_avail_bytes {job="$job",fstype=~"ext.?|xfs"}'\
                        '+(node_filesystem_size_bytes{job="$job",fstype=~"ext.?|xfs"}'\
                        '-node_filesystem_free_bytes{job="$job",fstype=~"ext.?|xfs"})))'
    server_min_cpu_usage = '(1 - max(rate(node_cpu_seconds_total{job="$job",mode="idle"}[10m])))*100'
    server_max_cpu_usage = '(1 - min(rate(node_cpu_seconds_total{job="$job",mode="idle"}[10m])))*100'
    server_min_mem_usage = '(1-max(node_memory_MemAvailable_bytes{job="$job"} / ' \
                           '(node_memory_MemTotal_bytes{job="$job"} - node_memory_HugePages_Total{job="$job"} * ' \
                           'node_memory_Hugepagesize_bytes{job="$job"}))) * 100'
    server_max_mem_usage = '(1-min(node_memory_MemAvailable_bytes{job="$job"} / ' \
                           '(node_memory_MemTotal_bytes{job="$job"} - node_memory_HugePages_Total{job="$job"} * ' \
                           'node_memory_Hugepagesize_bytes{job="$job"}))) * 100'
    server_min_disk_usage = 'min((node_filesystem_size_bytes{job="$job",fstype=~"ext.?|xfs"}'\
                            '-node_filesystem_free_bytes{job="$job",fstype=~"ext.?|xfs"}) *100'\
                            '/(node_filesystem_avail_bytes {job="$job",fstype=~"ext.?|xfs"}'\
                            '+(node_filesystem_size_bytes{job="$job",fstype=~"ext.?|xfs"}'\
                            '-node_filesystem_free_bytes{job="$job",fstype=~"ext.?|xfs"})))'
    server_max_disk_usage = 'max((node_filesystem_size_bytes{job="$job",fstype=~"ext.?|xfs"}'\
                            '-node_filesystem_free_bytes{job="$job",fstype=~"ext.?|xfs"}) *100'\
                            '/(node_filesystem_avail_bytes {job="$job",fstype=~"ext.?|xfs"}'\
                            '+(node_filesystem_size_bytes{job="$job",fstype=~"ext.?|xfs"}'\
                            '-node_filesystem_free_bytes{job="$job",fstype=~"ext.?|xfs"})))'

    tmpl_up = 'up{job="$job"} == 1'
    tmpl_down = 'up{job="$job"} == 0'
    tmpl_boot_time = '(time() - node_boot_time_seconds{job="$job"}) / 86400'     # day
    tmpl_cpu_count = 'count(node_cpu_seconds_total{job="$job", mode="system"}) by (instance)'
    tmpl_cpu_usage = '(1 - avg(rate(node_cpu_seconds_total{job="$job", mode="idle"}[1m])) by (instance)) * 100'
    tmpl_mem_size = 'node_memory_MemTotal_bytes{job="$job"} / 1073741824'  # GiB
    tmpl_mem_availabele = 'node_memory_MemAvailable_bytes{job="$job"} / 1073741824'   # GiB
    tmpl_root_dir_size = 'node_filesystem_size_bytes{job="$job", mountpoint="/"} / 1073741824'    # GiB
    tmpl_root_dir_avail_size = 'node_filesystem_avail_bytes{job="$job", mountpoint="/"} / 1073741824'  # GiB
    # MiB/s
    tmpl_net_rate_in = 'rate(node_network_receive_bytes_total{job="$job", device!~"lo|br_.*|vnet.*"}[1m]) * on(' \
                       'job, instance, device) (node_network_info{operstate="up"} == 1) / 8388608'
    tmpl_net_rate_out = 'rate(node_network_transmit_bytes_total{job="$job", device!~"lo|br_.*|vnet.*"}[1m]) * on(' \
                        'job, instance, device) (node_network_info{operstate="up"} == 1) / 8388608'

    @staticmethod
    def expression(tag: str, job: str = None):
        expression_query = tag
        if job:
            expression_query = Template(tag).substitute(job=job)

        return expression_query

    @staticmethod
    def render_expression(tmpl: str, job: str = None):
        expression_query = tmpl
        if job:
            expression_query = Template(tmpl).substitute(job=job)

        return expression_query

    def build_server_health_status_query(self, job: str = None):
        return self.expression(tag=self.server_health_status, job=job)

    def build_server_host_up_count_query(self, job: str = None):
        return self.expression(tag=self.server_host_up_count, job=job)

    def build_server_host_count_query(self, job: str = None):
        return self.expression(tag=self.server_host_count, job=job)

    def build_server_cpu_usage_query(self, job: str = None):
        return self.expression(tag=self.server_cpu_usage, job=job)

    def build_server_mem_usage_query(self, job: str = None):
        return self.expression(tag=self.server_mem_usage, job=job)

    def build_server_disk_usage_query(self, job: str = None):
        return self.expression(tag=self.server_disk_usage, job=job)

    def build_server_min_cpu_usage_query(self, job: str = None):
        return self.expression(tag=self.server_min_cpu_usage, job=job)

    def build_server_max_cpu_usage_query(self, job: str = None):
        return self.expression(tag=self.server_max_cpu_usage, job=job)

    def build_server_min_mem_usage_query(self, job: str = None):
        return self.expression(tag=self.server_min_mem_usage, job=job)

    def build_server_max_mem_usage_query(self, job: str = None):
        return self.expression(tag=self.server_max_mem_usage, job=job)

    def build_server_min_disk_usage_query(self, job: str = None):
        return self.expression(tag=self.server_min_disk_usage, job=job)

    def build_server_max_disk_usage_query(self, job: str = None):
        return self.expression(tag=self.server_max_disk_usage, job=job)


class MonitorServerQueryAPI:
    """
    response data example:
    {
        "status": "success",
        "data": {
            "resultType": "vector",
            "result": [
                {
                    "metric": {
                        "__name__": "node_memory_MemTotal_bytes",
                        "instance": "10.0.90.210:9100",
                        "job": "AIOPS-node",
                        "receive_cluster": "obs",
                        "receive_replica": "0",
                        "tenant_id": "default-tenant"
                    },
                    "value": [
                        1631585555,
                        "67522076672"
                    ]
                }
            ]
        }
    }
    """
    query_builder = ExpressionQuery()

    def server_health_status(self, provider: ThanosProvider, job: str):
        """
        :return:
        """
        expression_query = ExpressionQuery().build_server_health_status_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_host_up_count(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "13"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_host_up_count_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_host_count(self, provider: ThanosProvider, job: str):
        """
        :return:
        """
        expression_query = ExpressionQuery().build_server_host_count_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_cpu_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "2.0073197457862735"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_cpu_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_mem_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "26.093875641045372"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_mem_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_disk_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "26.84596010749737"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_disk_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_min_cpu_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "26.84596010749737"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_min_cpu_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_max_cpu_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "26.84596010749737"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_max_cpu_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_min_mem_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "26.84596010749737"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_min_mem_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_max_mem_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "26.84596010749737"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_max_mem_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_min_disk_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "26.84596010749737"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_min_disk_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def server_max_disk_usage(self, provider: ThanosProvider, job: str):
        """
        :return:
            [
                {
                    "metric": {},
                    "value": [
                        1631585555,
                        "26.84596010749737"
                    ]
                }
            ]
        """
        expression_query = ExpressionQuery().build_server_max_disk_usage_query(job=job)
        api_url = self._build_query_api(endpoint_url=provider.endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    def _request_query_api(self, url: str, expression_query: str):
        """
        :raises: Error
        """
        try:
            r = requests.post(url=url, data={'query': expression_query, 'time': int(time.time())}, timeout=(6, 30))
        except requests.exceptions.Timeout:
            raise errors.Error(message='monitor backend, server query api request timeout')
        except requests.exceptions.RequestException:
            raise errors.Error(message='monitor backend, server query api request error')
        data = r.json()
        if 300 > r.status_code >= 200:
            s = data.get('status')
            if s == 'success':
                return data['data']['result']

        raise self._build_error(r)

    @staticmethod
    def _build_error(r):
        data = r.json()
        msg = f"status: {r.status_code}, errorType: {data.get('errorType')}, error: {data.get('error')}"
        return errors.Error(message=msg)

    @staticmethod
    def _build_query_api(endpoint_url: str):
        endpoint_url = endpoint_url.rstrip('/')
        url = f'{endpoint_url}/api/v1/query'
        return url

    def query_tag(self, endpoint_url: str, tag_tmpl: str, job: str):
        """
        :return: []
        """
        expression_query = self.query_builder.render_expression(tmpl=tag_tmpl, job=job)
        api_url = self._build_query_api(endpoint_url=endpoint_url)
        return self._request_query_api(url=api_url, expression_query=expression_query)

    async def async_query_tag(self, endpoint_url: str, tag_tmpl: str, job: str):
        """
        :return:
        """
        expression_query = self.query_builder.render_expression(tmpl=tag_tmpl, job=job)
        api_url = self._build_query_api(endpoint_url=endpoint_url)
        query = parse.urlencode(query={'query': expression_query})
        api_url = f'{api_url}?{query}'
        return await self.async_request_query_api(url=api_url)

    @staticmethod
    async def async_request_query_api(url: str):
        """
        :raises: Error
        """
        try:
            async with aiohttp.ClientSession() as client:
                r = await client.get(url=url, timeout=aiohttp.ClientTimeout(connect=5, total=30))
        except requests.exceptions.Timeout:
            raise errors.Error(message='server backend,query api request timeout')
        except requests.exceptions.RequestException:
            raise errors.Error(message='server backend,query api request error')

        status_code = r.status
        if 300 > status_code >= 200:
            data = await r.json()
            s = data.get('status')
            if s == 'success':
                return data['data']['result']

        try:
            data = await r.json()
            msg = f"status: {status_code}, errorType: {data.get('errorType')}, error: {data.get('error')}"
        except Exception as e:
            text = await r.text()
            msg = f"status: {status_code}, error: {text}"

        raise errors.Error(message=msg)
