#!/usr/bin/env python
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from SSDBAdmin import app
from flask import render_template, request, make_response, redirect, url_for

from SSDBAdmin.model.ssdb_admin import SSDBObject
from SSDBAdmin.util import get_paging_tabs_info


@app.route('/ssdbadmin/zset/')
def zset_lists():
    """
    show the list of zset
    :return:
    """
    page_num = int(request.args.get('page_num', 1))
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 20)
    start = request.args.get('s', '')
    ssdb_object = SSDBObject(request)
    queue_list, has_next = ssdb_object.zset_list(start=start, page_num=page_num, page_size=int(page_size))
    select_arg = {'s': start, 'page_size': int(page_size)}
    resp = make_response(render_template('zset/zset.html', queue_list=queue_list, has_next=has_next,
                                         page_num=page_num, select_arg=select_arg, active='zset'))
    return resp


@app.route('/ssdbadmin/zset/zset/', methods=['GET', 'POST'])
def zset_zset():
    """
    add item to queue(support back and front)
    :return:
    """
    if request.method == 'GET':
        queue_name = request.args.get('n')
        return render_template('queue/queue_qpush.html', queue_name=queue_name, active='queue')
    else:
        queue_name = request.form.get('queue_name')
        push_type = request.form.get('type')
        item = request.form.get('item')
        ssdb_object = SSDBObject(request)
        ssdb_object.queue_qpush(queue_name, item, push_type)
        return redirect(url_for('queue_qrange', n=queue_name))
