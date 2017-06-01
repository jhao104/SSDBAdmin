#!/usr/bin/env python

from SSDBAdmin.setting import servers
from SSDBAdmin.util import get_paging_tabs_info

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
        # self.__init_arg(request)

    # def __init_arg(self, request):
    #     if 'SIZE' in request.cookies:
    #         self.limit = int(request.cookies.get('SIZE'))
    #     else:
    #         self.limit = 20

    def queue_list(self, start, end, page_num, page_size):
        all_list = self.__conn.qlist(name_start=start, name_end=end, limit=(page_num + 1) * page_size)
        page_count, page_num = get_paging_tabs_info(data_count=len(all_list), page_no=page_num, page_row_num=page_size)
        has_next = True if page_count > page_num else False
        queue_list = map(lambda queue_name: {'name': queue_name, 'size': self.__conn.qsize(queue_name)},
                         all_list[(page_num - 1) * page_size: page_num * page_size - 1])
        return queue_list, has_next

    def queue_qpush(self, queue_name, item, push_type):
        if push_type == 'front':
            self.__conn.qpush_front(queue_name, item)
        else:
            # push_type = 'back'
            self.__conn.qpush_back(queue_name, item)

    def queue_qpop(self, queue_name, number, pop_type):
        """
        Remove the first or last ``number`` item of the queue ``name``
        :param queue_name:
        :param number:
        :param pop_type:
        :return:
        """
        if pop_type == 'front':
            self.__conn.qpop_front(queue_name, int(number))
        else:
            # pop_type = 'back
            self.__conn.qpop_back(queue_name, int(number))

    def queue_qrange(self, queue_name, offset, limit):
        """
        Return a ``limit`` slice of the queue ``name`` at position ``offset``
        :param queue_name:
        :param offset:
        :param limit:
        :return:
        """
        return self.__conn.qrange(queue_name, int(offset), int(limit))

    def queue_size(self, queue_name):
        """
        length of queue
        :param queue_name:
        :return:
        """
        return self.__conn.qsize(queue_name)

    def queue_qget(self, queue_name, index):
        """
        Get the item of ``index`` within the queue_name
        :param queue_name:
        :param index:
        :return:
        """
        return self.__conn.qget(queue_name, int(index))
