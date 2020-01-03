# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     hash
   Description :   hash view
   Author :        JHao
   date：          2018/9/3
-------------------------------------------------
   Change Activity:
                   2018/9/3: hash view
-------------------------------------------------
"""
__author__ = 'JHao'

from SSDBAdmin import app
from SSDBAdmin.model.SSDBClient import SSDBClient
from flask import render_template, request, make_response, redirect, url_for


@app.route('/ssdbadmin/hash/')
def hashLists():
    """
    show the list of hash
    :return:
    """
    page_num = int(request.args.get('page_num', 1))
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 10)
    start = request.args.get('start', '')
    end = request.args.get('end', '')

    db_client = SSDBClient(request)
    hash_list, has_next = db_client.hashList(name_start=start, name_end=end, page_num=page_num,
                                             page_size=int(page_size))
    select_arg = {'start': start, 'end': end, 'page_size': int(page_size)}
    resp = make_response(render_template('hash/hash.html', hash_list=hash_list, has_next=has_next,
                                         has_prev=page_num > 1,
                                         page_num=page_num, select_arg=select_arg, active='hash'))
    resp.set_cookie("SIZE", str(page_size), httponly=True, samesite='Lax')
    return resp


@app.route('/ssdbadmin/hash/scan')
def hashScan():
    """
    show the list of hash item
    :return:
    """
    name = request.args.get('name')
    key_start = request.args.get('start', '')
    page_size = request.args.get('page_size')
    page_number = int(request.args.get('page_num', 1))
    if not page_size:
        page_size = request.cookies.get('SIZE', 10)
    db_client = SSDBClient(request)
    limit = int(page_size) * page_number
    item_list = db_client.hashScan(name, key_start, "", limit=limit + 1)
    if len(item_list) > limit:
        has_next = True
        item_list = item_list[-int(page_size) - 1:-1]
    else:
        has_next = False
        item_list = item_list[-int(page_size):]
    select_arg = {'page_size': int(page_size), 'start': key_start}
    resp = make_response(render_template('hash/hash_scan.html',
                                         item_list=item_list,
                                         page_num=page_number,
                                         key_start=key_start,
                                         name=name,
                                         has_next=has_next,
                                         has_prev=page_number > 1,
                                         select_arg=select_arg,
                                         active='hash'))
    resp.set_cookie('SIZE', str(page_size), httponly=True, samesite='Lax')
    return resp


@app.route('/ssdbadmin/hash/set', methods=['GET', 'POST'])
def hashSet():
    """
    Set the value of key within the hash_name
    :return:
    """
    if request.method == 'GET':
        name = request.args.get('name')
        key = request.args.get('key', '')
        value = request.args.get('value', '')
        return render_template('hash/hash_set.html', name=name, key=key, value=value, active='hash')
    else:
        name = request.form.get('name')
        key = request.form.get('key')
        value = request.form.get('value')
        SSDBClient(request).hashSet(name, key, value)
        return redirect(url_for('hashScan', name=name))
    pass


@app.route('/ssdbadmin/hash/del/', methods=['GET', 'POST'])
def hashDel():
    """
    remove keys from zset_name
    :return:
    """
    if request.method == 'GET':
        name = request.args.get('name')
        key = request.args.get('key')
        keys = request.args.getlist('keys')
        if key:
            keys.append(key)
        return render_template('hash/hash_del.html', keys=keys, name=name, active='hash')
    else:
        keys = request.form.getlist('key')
        name = request.form.get('name')
        SSDBClient(request).hashDel(name, *keys)
        return redirect(url_for('hashScan', name=name))


@app.route('/ssdbadmin/hash/clear/', methods=['GET', 'POST'])
def hashClear():
    """
    delete  the specified hash data
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name')
        SSDBClient(request).hashClear(name)
        return redirect(url_for('hashLists'))
    else:
        name = request.args.get('name')
        return render_template('hash/hash_clear.html', name=name, active='hash')
    pass


@app.route('/ssdbadmin/hash/get/')
def hashGet():
    """
    show an item info from hash
    :return:
    """
    name = request.args.get('name')
    key = request.args.get('key')
    value = SSDBClient(request).hashGet(name, key)
    return render_template('hash/hash_get.html', name=name, value=value, key=key, active='hash')
