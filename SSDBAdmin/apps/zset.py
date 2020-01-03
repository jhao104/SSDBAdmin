# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     zset
   Description :   zset view
   Author :        JHao
   date：          2018/8/30
-------------------------------------------------
   Change Activity:
                   2018/8/30: zset view
-------------------------------------------------
"""
__author__ = 'JHao'

from SSDBAdmin import app
from SSDBAdmin.model.SSDBClient import SSDBClient
from SSDBAdmin.utils.paginator import getPagingTabsInfo, getPageNumberInfo
from flask import render_template, request, make_response, redirect, url_for


@app.route('/ssdbadmin/zset/')
def zsetLists():
    """
    show the items of zset
    :return:
    """
    page_num = int(request.args.get('page_num', 1))
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 20)
    start = request.args.get('start', '')
    db_client = SSDBClient(request)
    zset_list, has_next = db_client.zsetList(start=start, page_num=page_num, page_size=int(page_size))
    select_arg = {'start': start, 'page_size': int(page_size)}
    resp = make_response(render_template('zset/zset.html', zset_list=zset_list, has_next=has_next,
                                         has_prev=page_num > 1,
                                         page_num=page_num, select_arg=select_arg, active='zset'))
    resp.set_cookie('SIZE', str(page_size), httponly=True, samesite='Lax')
    return resp


@app.route('/ssdbadmin/zset/set/', methods=['GET', 'POST'])
def zsetSet():
    """
    add item to zset
    :return:
    """
    if request.method == 'GET':
        name = request.args.get('name')
        key = request.args.get('key', '')
        score = request.args.get('score', '')
        return render_template('zset/zset_set.html', name=name, key=key, score=score, active='zset')
    else:
        name = request.form.get('name')
        key = request.form.get('key')
        score = request.form.get('score')
        try:
            score = int(score)
        except ValueError:
            score = 0
        SSDBClient(request).zsetSet(name, key, score)
        return redirect(url_for('zsetRange', name=name))


@app.route('/ssdbadmin/zset/range/')
def zsetRange():
    """
    show the list of item from zst
    :return:
    """
    set_name = request.args.get('name')
    start = request.args.get('start', "")
    page_num = request.args.get('page_num', 1)
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 10)

    db_object = SSDBClient(request)
    item_total = db_object.zsetSize(set_name)
    page_count, page_num = getPagingTabsInfo(item_total, page_num, page_size)
    offset = (page_num - 1) * int(page_size)
    if start:
        rank = db_object.zsetRank(set_name, start)
        if rank:
            page_num = getPageNumberInfo(rank, page_count, page_size)
            offset = (page_num - 1) * int(page_size)

    item_list = db_object.zsetRange(set_name, offset=offset, limit=page_size)
    select_arg = {'page_size': int(page_size)}
    resp = make_response(render_template('zset/zset_range.html',
                                         item_list=item_list,
                                         name=set_name,
                                         page_num=int(page_num),
                                         page_count=page_count,
                                         select_arg=select_arg,
                                         start=start,
                                         active='zset'))
    resp.set_cookie('SIZE', str(page_size), httponly=True, samesite='Lax')
    return resp


@app.route('/ssdbadmin/zset/del/', methods=['GET', 'POST'])
def zsetDel():
    """
    remove keys from zset
    :return:
    """
    if request.method == 'GET':
        name = request.args.get('name')
        key = request.args.get('key')
        keys = request.args.getlist('keys')
        if key:
            keys.append(key)
        return render_template('zset/zset_del.html', keys=keys, name=name, active='zset')
    else:
        keys = request.form.getlist('key')
        name = request.form.get('name')
        SSDBClient(request).zsetDel(name, *keys)
        return redirect(url_for('zsetRange', name=name))


@app.route('/ssdbadmin/zset/zclear/', methods=['GET', 'POST'])
def zsetClear():
    """
    delete  the specified zset data
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name')
        SSDBClient(request).zsetClear(name)
        return redirect(url_for('zsetLists'))
    else:
        queue_name = request.args.get('name')
        return render_template('zset/zset_clear.html', name=queue_name, active='zset')


@app.route('/ssdbadmin/zset/zget/')
def zset_zget():
    """
    show item info from zset
    :return:
    """
    name = request.args.get('name')
    key = request.args.get('key')
    score = SSDBClient(request).zsetGet(name, key)
    return render_template('zset/zset_get.html', name=name, score=score, key=key, active='zset')
