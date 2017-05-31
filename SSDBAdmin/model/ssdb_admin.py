#!/usr/bin/env python

from SSDBAdmin.setting import servers

from ssdb.connection import BlockingConnectionPool
from ssdb import SSDB


def get_sa_server(request):
    if 'SSDBADMINSERVER' in request.cookies:
        host, port = request.cookies.get('SSDBADMINSERVER').split(':')
    else:
        server = servers[0]
        host = server.get('host', 'localhost')
        port = server.get('port', 8888)
    return host, port


class SSDBObject(object):
    def __init__(self, request):
        host, port = get_sa_server(request)
        self.__conn = SSDB(connection_pool=BlockingConnectionPool(host=host, port=int(port)))
        self.__init_arg(request)

    def __init_arg(self, request):
        if 'psa_size' in request.cookies:
            self.limit = int(request.cookies.get('psa_size'))
        else:
            self.limit = 20

    def queue_list(self, start, limit=None):
        if limit:
            self.limit = limit
        queue_name_list = self.__conn.qlist(name_start=start, name_end='', limit=self.limit)
        queue_list = map(lambda queue_name: {'name': queue_name, 'size': self.__conn.qsize(queue_name)},
                         queue_name_list)
        return queue_list

    def queue_qpush(self, queue_name, item, push_type):
        if push_type == 'front':
            self.__conn.qpush_front(queue_name, item)
        else:
            # push_type = 'back'
            self.__conn.qpush_back(queue_name, item)
