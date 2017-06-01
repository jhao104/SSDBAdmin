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
    zset_list, has_next = ssdb_object.zset_list(start=start, page_num=page_num, page_size=int(page_size))
    select_arg = {'s': start, 'page_size': int(page_size)}
    resp = make_response(render_template('zset/zset.html', zset_list=zset_list, has_next=has_next,
                                         page_num=page_num, select_arg=select_arg, active='zset'))
    return resp


@app.route('/ssdbadmin/zset/zset/', methods=['GET', 'POST'])
def zset_zset():
    """
    add item to queue(support back and front)
    :return:
    """
    if request.method == 'GET':
        name = request.args.get('n')
        return render_template('zset/zset_zset.html', name=name, active='zset')
    else:
        name = request.form.get('n')
        key = request.form.get('k')
        score = request.form.get('s')
        try:
            score = int(score)
        except ValueError:
            score = 0
        ssdb_object = SSDBObject(request)
        ssdb_object.zset_zset(name, key, score)
        return redirect(url_for('zset_zscan', n=name))


@app.route('/ssdbadmin/zset/zscan/')
def zset_zscan():
    """
    show the list of item from queue
    :return:
    """
    name = request.args.get('n')
    key_start = request.args.get('s', '')
    tp = request.args.get('t')
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 20)
    ssdb_object = SSDBObject(request)
    has_next, has_prev, item_list = ssdb_object.zset_zscan(name, key_start, tp, limit=int(page_size))
    select_arg = {'page_size': int(page_size), 's': item_list[-1].get('key') if item_list else ''}
    resp = make_response(render_template('zset/zset_zscan.html',
                                         item_list=item_list,
                                         name=name,
                                         page_num=1,
                                         key_start=key_start,
                                         has_next=has_next,
                                         has_prev=has_prev,
                                         select_arg=select_arg,
                                         active='zset'))
    resp.set_cookie('SIZE', str(page_size))
    return resp