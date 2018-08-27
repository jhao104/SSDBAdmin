# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     SSDBClient
   Description :   SSDBClient
   Author :        JHao
   date：          2018/8/24
-------------------------------------------------
   Change Activity:
                   2018/8/24: SSDBClient
-------------------------------------------------
"""
__author__ = 'JHao'

from redis.connection import BlockingConnectionPool
from SSDBAdmin.setting import DB_CONFIG
from redis import Redis


def getSAServer(request):
    """
    Get key `SSDBADMIN_SERVER` from request’s cookie
    Args:
        request: flask request
    Returns:
        current ssdb's host and post
    """
    if 'SSDBADMIN_SERVER' in request.args:
        host, port = request.args.get('SSDBADMIN_SERVER').split(':')
    elif 'SSDBADMINSERVER' in request.cookies:
        host, port = request.cookies.get('SSDBADMINSERVER').split(':')
    else:
        server = DB_CONFIG[0]
        host = server.get('host', 'localhost')
        port = server.get('port', 8888)
    return host, port


class SSDBClient(object):
    def __init__(self, request):
        host, port = getSAServer(request)
        self.__conn = Redis(connection_pool=BlockingConnectionPool(host=host, port=int(port)))

    def serverInfo(self):
        """
        DB service info(version/links/size/stats ...)
        Returns:
            info message as dict
        """
        info_list = [_.decode() for _ in self.__conn.execute_command('info')]
        version = info_list[2]
        links = info_list[4]
        total_calls = info_list[6]
        db_size = info_list[8]
        bin_logs = info_list[10]
        service_key_range = info_list[12]
        data_key_range = info_list[14]
        stats = info_list[16]

        def _parseDiskUsage(_stats):
            return sum([int(each.split()[2]) for each in _stats.split('\n')[3:-1]])

        return {'info_list': info_list, 'version': version, 'links': links, 'total_calls': total_calls,
                'db_size': db_size, 'bin_logs': bin_logs, 'service_key_range': service_key_range,
                'data_key_range': data_key_range,
                'stats': stats, 'disk_usage': _parseDiskUsage(stats)}
