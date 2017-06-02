#!/usr/bin/env python
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from SSDBAdmin import app
from flask import render_template, request, make_response, redirect, url_for

from SSDBAdmin.model.ssdb_admin import SSDBObject


@app.route('/ssdbadmin/hash/')
def hash_lists():
    """
    show the list of hash
    :return:
    """
    key_start = request.args.get('s', '')
    tp = request.args.get('t')
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 20)
    ssdb_object = SSDBObject(request)
    has_next, has_prev, hash_list = ssdb_object.hash_list(key_start, tp, limit=int(page_size))
    prev_s, next_s = '', ''
    if hash_list:
        next_s = hash_list[-1].get('name')
        prev_s = hash_list[0].get('name')
    select_arg = {'page_size': int(page_size), 'prev_s': prev_s, 'next_s': next_s, 's': key_start}
    resp = make_response(render_template('hash/hash.html',
                                         hash_list=hash_list,
                                         page_num=1,
                                         has_next=has_next,
                                         has_prev=has_prev,
                                         select_arg=select_arg,
                                         active='hash'))
    resp.set_cookie('SIZE', str(page_size))
    return resp


@app.route('/ssdbadmin/hash/hscan')
def hash_hscan():
    """
    show the list of hash item
    :return:
    """
    name = request.args.get('n')
    key_start = request.args.get('s', '')
    tp = request.args.get('t')
    page_size = request.args.get('page_size')
    if not page_size:
        page_size = request.cookies.get('SIZE', 20)
    ssdb_object = SSDBObject(request)
    has_next, has_prev, item_list = ssdb_object.hash_hscan(name, key_start, tp, limit=int(page_size))
    prev_s, next_s = '', ''
    if item_list:
        next_s = item_list[-1].get('key')
        prev_s = item_list[0].get('key')
    select_arg = {'page_size': int(page_size), 'prev_s': prev_s, 'next_s': next_s, 's': key_start}
    resp = make_response(render_template('hash/hash_hscan.html',
                                         item_list=item_list,
                                         page_num=1,
                                         key_start=key_start,
                                         name=name,
                                         has_next=has_next,
                                         has_prev=has_prev,
                                         select_arg=select_arg,
                                         active='hash'))
    resp.set_cookie('SIZE', str(page_size))
    return resp
