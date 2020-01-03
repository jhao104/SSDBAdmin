# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     kv
   Description :   kv view
   Author :        JHao
   date：          2018/9/4
-------------------------------------------------
   Change Activity:
                   2018/9/4: kv view
-------------------------------------------------
"""
__author__ = 'JHao'

from SSDBAdmin import app
from SSDBAdmin.model.SSDBClient import SSDBClient
from flask import render_template, request, make_response, redirect, url_for


@app.route('/ssdbadmin/kv/scan')
def kvScan():
    """
    show the list of kv item
    """
    key_start = request.args.get('start', '')
    page_size = request.args.get('page_size')
    page_number = int(request.args.get('page_num', 1))
    if not page_size:
        page_size = request.cookies.get('SIZE', 10)
    db_client = SSDBClient(request)
    limit = int(page_size) * page_number
    item_list = db_client.kvScan(key_start, "", limit=limit + 1)
    if len(item_list) > limit:
        has_next = True
        item_list = item_list[-int(page_size) - 1:-1]
    else:
        has_next = False
        item_list = item_list[-int(page_size):]
    select_arg = {'page_size': int(page_size), 'start': key_start}
    resp = make_response(render_template('kv/kv_scan.html',
                                         item_list=item_list,
                                         page_num=page_number,
                                         key_start=key_start,
                                         has_next=has_next,
                                         has_prev=page_number > 1,
                                         select_arg=select_arg,
                                         active='kv'))
    resp.set_cookie('SIZE', str(page_size), httponly=True, samesite='Lax')
    return resp


@app.route('/ssdbadmin/kv/get/')
def kvGet():
    """
    show a kv info
    """
    key = request.args.get('key')
    value, ttl = SSDBClient(request).kvGet(key)
    return render_template('kv/kv_get.html', key=key, value=value, ttl=ttl, active='kv')
    pass


@app.route('/ssdbadmin/kv/set/', methods=['GET', 'POST'])
def kvSet():
    """
    add item to kv
    """
    if request.method == 'GET':
        key = request.args.get('key', '')
        value = request.args.get('value', '')
        return render_template('kv/kv_set.html', key=key, value=value, active='kv')
    else:
        key = request.form.get('key')
        value = request.form.get('value')
        SSDBClient(request).kvSet(key, value)
        return redirect(url_for('kvScan'))


@app.route('/ssdbadmin/kv/del/', methods=['GET', 'POST'])
def kvDel():
    """
    remove keys from kv
    :return:
    """
    if request.method == 'GET':
        key = request.args.get('key')
        keys = request.args.getlist('keys')
        if key:
            keys.append(key)
        return render_template('kv/kv_del.html', keys=keys, active='kv')
    else:
        keys = request.form.getlist('key')
        if keys:
            SSDBClient(request).kvDel(*keys)
        return redirect(url_for('kvScan'))
