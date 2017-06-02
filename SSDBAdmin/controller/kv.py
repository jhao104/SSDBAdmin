#!/usr/bin/env python
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from SSDBAdmin import app
from flask import render_template, request, make_response, redirect, url_for

from SSDBAdmin.model.ssdb_admin import SSDBObject


@app.route('/ssdbadmin/kv/scan')
def kv_scan():
    """
    show the list of kv item
    :return:
    """
    key_start = request.args.get('s', '')
    tp = request.args.get('t')
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 20)
    ssdb_object = SSDBObject(request)
    has_next, has_prev, item_list = ssdb_object.kv_kscan(key_start, tp, limit=int(page_size))
    prev_s, next_s = '', ''
    if item_list:
        next_s = item_list[-1].get('key')
        prev_s = item_list[0].get('key')
    select_arg = {'page_size': int(page_size), 'prev_s': prev_s, 'next_s': next_s, 's': key_start}
    resp = make_response(render_template('kv/kv_kscan.html',
                                         item_list=item_list,
                                         page_num=1,
                                         key_start=key_start,
                                         has_next=has_next,
                                         has_prev=has_prev,
                                         select_arg=select_arg,
                                         active='kv'))
    resp.set_cookie('SIZE', str(page_size))
    return resp


@app.route('/ssdbadmin/kv/get/')
def kv_get():
    """
    show a kv info
    :return:
    """
    key = request.args.get('k')
    ssdb_object = SSDBObject(request)
    value = ssdb_object.kv_get(key)
    return render_template('kv/kv_kget.html', key=key, value=value, active='kv')


@app.route('/ssdbadmin/kv/set/', methods=['GET', 'POST'])
def kv_set():
    """
    add item to queue(support back and front)
    :return:
    """
    if request.method == 'GET':
        key = request.args.get('k', '')
        value = request.args.get('v', '')
        return render_template('kv/kv_set.html', key=key, value=value, active='kv')
    else:
        key = request.form.get('k')
        value = request.form.get('v')
        ssdb_object = SSDBObject(request)
        ssdb_object.kv_set(key, value)
        return redirect(url_for('kv_scan'))


@app.route('/ssdbadmin/kv/del/', methods=['GET', 'POST'])
def kv_del():
    """
    remove keys from kv
    :return:
    """
    if request.method == 'GET':
        key = request.args.get('k')
        keys = request.args.getlist('keys')
        if key:
            keys.append(key)
        return render_template('kv/kv_del.html', keys=keys, active='kv')
    else:
        keys = request.form.getlist('k')
        ssdb_object = SSDBObject(request)
        ssdb_object.kv_del(*keys)
        return redirect(url_for('kv_scan'))
