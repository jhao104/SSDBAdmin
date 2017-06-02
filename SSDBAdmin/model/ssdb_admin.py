#!/usr/bin/env python

from SSDBAdmin.setting import servers
from SSDBAdmin.util import get_paging_tabs_info

from ssdb.connection import BlockingConnectionPool
from ssdb import SSDB


def get_sa_server(request):
    if 'SSDBADMIN_SERVER' in request.args:
        host, port = request.args.get('SSDBADMIN_SERVER').split(':')
    elif 'SSDBADMINSERVER' in request.cookies:
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

    def server_info(self):
        info_list = self.__conn.execute_command('info')
        version = info_list[3]
        links = info_list[5]
        total_calls = info_list[7]
        dbsize = info_list[9]
        binlogs = info_list[11]
        serv_key_range = info_list[13]
        data_key_range = info_list[15]
        stats = info_list[17]

        def parse_disk_usage(stats):
            return sum([int(each.split()[2]) for each in stats.split('\n')[3:-1]])

        return {'info_list': info_list, 'version': version, 'links': links, 'total_calls': total_calls,
                'dbsize': dbsize, 'binlogs': binlogs, 'serv_key_range': serv_key_range,
                'data_key_range': data_key_range,
                'stats': stats, 'disk_usage': parse_disk_usage(stats)}

    # ########## Queue operate ##########
    def queue_list(self, start, end, page_num, page_size):
        """
        return a list of queue info between start and end
        :param start: The lower bound(not included) of keys to be returned, empty string ``''`` means -inf
        :param end: The upper bound(included) of keys to be returned, empty string ``''`` means +inf
        :param page_num:
        :param page_size:
        :return:
        """
        all_list = self.__conn.qlist(name_start=start, name_end=end, limit=(page_num + 1) * page_size)
        page_count, page_num = get_paging_tabs_info(data_count=len(all_list), page_no=page_num, page_row_num=page_size)
        has_next = True if page_count > page_num else False
        queue_list = map(lambda queue_name: {'name': queue_name, 'size': self.__conn.qsize(queue_name)},
                         all_list[(page_num - 1) * page_size: page_num * page_size - 1])
        return queue_list, has_next

    def queue_qpush(self, queue_name, item, push_type):
        """
        Push item onto the back(front) of the queue_name
        :param queue_name:
        :param item:
        :param push_type: back or front
        :return:
        """
        if push_type == 'front':
            self.__conn.qpush_front(queue_name, item)
        else:
            # push_type = 'back'
            self.__conn.qpush_back(queue_name, item)

    def queue_qpop(self, queue_name, number, pop_type):
        """
        Remove the first or last number item of the queue_name
        :param queue_name:
        :param number: item number
        :param pop_type:back or front
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

    def queue_qclear(self, queue_name):
        """
        **Clear&Delete** the queue specified by queue_name`
        :param queue_name:
        :return:
        """
        return self.__conn.qclear(queue_name)

    # ########## Zset operate ##########

    def zset_list(self, start, page_num, page_size):
        """
        return a list of zset info
        :param start:
        :param page_num:
        :param page_size:
        :return:
        """
        all_list = self.__conn.zlist(name_start=start, name_end='', limit=(page_num + 1) * page_size)
        page_count, page_num = get_paging_tabs_info(data_count=len(all_list), page_no=page_num, page_row_num=page_size)
        has_next = True if page_count > page_num else False
        zset_list = map(lambda zset_name: {'name': zset_name, 'size': self.__conn.zsize(zset_name)},
                        all_list[(page_num - 1) * page_size: page_num * page_size - 1])
        return zset_list, has_next

    def zset_zset(self, zset_name, key, score):
        """
        Set the score of ``key`` from the zset ``name`` to ``score``
        :param zset_name:
        :param key:
        :param score:
        :return:
        """
        return self.__conn.zset(zset_name, key, score)

    def zset_zsize(self, zset_name):
        """
        Return the number of elements in zset
        :param zset_name:
        :return:
        """
        return self.__conn.zsize(zset_name)

    def zset_zscan(self, zset_name, key, tp, limit):
        """
        Return a dict mapping key/score
        :param zset_name:
        :param key:
        :param tp:
        :param limit:
        :return:
        """
        next = self.__conn.zscan(name=zset_name, key_start=key, score_start='', score_end='', limit=limit + 1)
        prev = self.__conn.zrscan(name=zset_name, key_start=key, score_start='', score_end='', limit=limit + 1)
        item_dict = prev if tp == 'prev' else next
        has_next = False if len(next) <= limit and tp == 'next' else True
        has_prev = False if len(prev) <= limit and tp == 'prev' else True
        if not tp:
            has_next = False if len(next) <= limit else True
            has_prev = False
        item_list = [{'key': key, 'score': score} for key, score in item_dict.iteritems()]
        if tp == 'prev':
            item_list = item_list[::-1]
        return has_next, has_prev, item_list[:-1] if len(item_list) > limit else item_list

    def zset_del(self, zset_name, *keys):
        """
        remove keys from zset_name
        :param zset_name:
        :param keys:
        :return:
        """
        return self.__conn.multi_zdel(zset_name, *keys)

    def zset_zclear(self, zset_name):
        """
        **Clear&Delete** the zset specified by zset_name
        :param zset_name:
        :param keys:
        :return:
        """
        return self.__conn.zclear(zset_name)

    # ################ Hash operate #############

    def hash_list(self, start_name, tp, limit):
        """
        return  Return a list of the top ``limit`` hash's name start with start_name
        :param start_name:
        :param tp: next or prev  next(ascending) prev(descending)
        :param limit:
        :return:
        """
        next = self.__conn.hlist(name_start=start_name, name_end='', limit=limit + 1)
        prev = self.__conn.hrlist(name_start=start_name, name_end='', limit=limit + 1)
        item_list = prev if tp == 'prev' else next
        has_next = False if len(next) <= limit and tp == 'next' else True
        has_prev = False if len(prev) <= limit and tp == 'prev' else True
        if not tp:
            has_next = False if len(next) <= limit else True
            has_prev = False
        if tp == 'prev':
            item_list = item_list[::-1]
        hash_list = map(lambda hash_name: {'name': hash_name, 'size': self.__conn.hsize(hash_name)},
                        item_list)
        return has_next, has_prev, hash_list[:-1] if len(hash_list) > limit else hash_list

    def hash_hscan(self, hash_name, start_key, tp, limit):
        """
        Return a dict mapping key/value in the top ``limit`` keys start with start_key within hash_name
        :param hash_name:
        :param start_key:
        :param tp: next or prev  next(ascending) prev(descending)
        :param limit:
        :return:
        """
        next = self.__conn.hscan(hash_name, key_start=start_key, key_end='', limit=limit + 1)
        prev = self.__conn.hrscan(hash_name, key_start=start_key, key_end='', limit=limit + 1)
        item_dict = prev if tp == 'prev' else next
        has_next = False if len(next) <= limit and tp == 'next' else True
        has_prev = False if len(prev) <= limit and tp == 'prev' else True
        if not tp:
            has_next = False if len(next) <= limit else True
            has_prev = False
        item_list = [{'key': key, 'value': value} for key, value in item_dict.iteritems()]
        if tp == 'prev':
            item_list = item_list[::-1]
        return has_next, has_prev, item_list[:-1] if len(item_list) > limit else item_list

    def hash_hset(self, hash_name, key, value):
        """
         Set the value of key within the hash_name
        :param hash_name:
        :param key:
        :param value:
        :return:
        """
        self.__conn.hset(hash_name, key, value)


if __name__ == '__main__':
    s = SSDB(connection_pool=BlockingConnectionPool(host='42.123.99.64', port=int(8889)))
    print s.execute_command('info')[17]
