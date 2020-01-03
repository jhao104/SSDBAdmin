# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     queue
   Description :   queue view
   Author :        JHao
   date：          2018/8/27
-------------------------------------------------
   Change Activity:
                   2018/8/27: queue view
-------------------------------------------------
"""
__author__ = 'JHao'

from SSDBAdmin import app
from SSDBAdmin.model.SSDBClient import SSDBClient
from SSDBAdmin.utils.paginator import getPagingTabsInfo, getPageNumberInfo
from flask import render_template, request, make_response, redirect, url_for


@app.route('/ssdbadmin/queue/')
def queueLists():
    """
    show the items of queue/list
    :return:
    """
    page_num = int(request.args.get('page_num', 1))
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 10)
    start = request.args.get('start', '')
    end = request.args.get('end', '')

    db_client = SSDBClient(request)
    queue_list, has_next = db_client.queueList(name_start=start, name_end=end, page_num=page_num,
                                               page_size=int(page_size))
    select_arg = {'start': start, 'end': end, 'page_size': int(page_size)}
    resp = make_response(render_template('queue/queue.html', queue_list=queue_list, has_next=has_next,
                                         has_prev=page_num > 1,
                                         page_num=page_num, select_arg=select_arg, active='queue'))
    resp.set_cookie("SIZE", str(page_size), httponly=True, samesite='Lax')
    return resp


@app.route('/ssdbadmin/queue/push/', methods=['GET', 'POST'])
def queuePush():
    """
    add item to queue(support back/front type)
    Returns:
    """
    if request.method == 'GET':
        queue_name = request.args.get('name')
        return render_template('queue/queue_push.html', queue_name=queue_name, active='queue')
    elif request.method == "POST":
        queue_name = request.form.get('queue_name')
        push_type = request.form.get('type')
        item = request.form.get('item')
        SSDBClient(request).queuePush(queue_name, item, push_type)
        return redirect(url_for('queueRange', name=queue_name))


@app.route('/ssdbadmin/queue/pop/', methods=['GET', 'POST'])
def queuePop():
    """
    pop item(s) from queue (support back/front type)
    :return:
    """
    if request.method == 'GET':
        queue_name = request.args.get('name')
        return render_template('queue/queue_pop.html', queue_name=queue_name, active='queue')
    else:
        queue_name = request.form.get('name')
        pop_type = request.form.get('type')
        number = request.form.get('number')
        SSDBClient(request).queuePop(queue_name, number, pop_type)
        return redirect(url_for('queueRange', name=queue_name))


@app.route('/ssdbadmin/queue/range/')
def queueRange():
    """
    show the list of item from queue
    :return:
    """
    queue_name = request.args.get('name')
    start = request.args.get('start')
    page_num = request.args.get('page_num', 1)
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', "10")

    db_object = SSDBClient(request)
    item_total = db_object.queueSize(queue_name)
    page_count, page_num = getPagingTabsInfo(item_total, page_num, page_size)
    offset = (page_num - 1) * int(page_size)
    if start and start.isdigit():
        page_num = getPageNumberInfo(int(start), page_count, page_size)
        offset = (page_num - 1) * int(page_size)
    else:
        start = offset

    item_list = db_object.queueRange(queue_name, offset=offset, limit=page_size)
    select_arg = {'page_size': int(page_size)}
    resp = make_response(render_template('queue/queue_range.html',
                                         item_list=item_list,
                                         name=queue_name,
                                         page_num=int(page_num),
                                         page_count=page_count,
                                         select_arg=select_arg,
                                         start_index=offset,
                                         start=start,
                                         data_total=item_total,
                                         active='queue'))
    resp.set_cookie('SIZE', page_size, httponly=True, samesite='Lax')
    return resp


@app.route('/ssdbadmin/queue/get/')
def queueGet():
    """
    show an item info from queue
    :return:
    """
    queue_name = request.args.get('name')
    index = request.args.get('index')
    item = SSDBClient(request).queueGet(queue_name, index)
    return render_template('queue/queueGet.html', name=queue_name, item=item, index=index, active='queue')


@app.route('/ssdbadmin/queue/clear/', methods=['GET', 'POST'])
def queueClear():
    """
    delete the specified queue
    :return:
    """
    if request.method == 'POST':
        queue_name = request.form.get('name')
        SSDBClient(request).queueClear(queue_name)
        return redirect(url_for('queueLists'))
    else:
        queue_name = request.args.get('name')
        return render_template('queue/queue_clear.html', name=queue_name, active='queue')
