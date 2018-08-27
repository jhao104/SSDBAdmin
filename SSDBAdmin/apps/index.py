# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     index
   Description :
   Author :        JHao
   date：          2018/8/24
-------------------------------------------------
   Change Activity:
                   2018/8/24:
-------------------------------------------------
"""
__author__ = 'JHao'

from SSDBAdmin import app
from SSDBAdmin.setting import DB_CONFIG, VERSION
from SSDBAdmin.model.SSDBClient import getSAServer, SSDBClient
from flask import render_template, request, make_response, redirect, url_for


@app.route('/ssdbadmin/')
def index():
    host, port = getSAServer(request)
    server_info = SSDBClient(request).serverInfo()
    resp = make_response(render_template('index.html', server_info=server_info))
    resp.set_cookie('SSDBADMINSERVER', '{host}:{port}'.format(host=host, port=port))
    return resp


@app.context_processor
def commonParam():
    host, port = getSAServer(request)
    server_list = ['{}:{}'.format(server.get('host'), server.get('port')) for server in DB_CONFIG]
    current_server = '{}:{}'.format(host, port)
    return dict(server_list=server_list, current_server=current_server, version=VERSION)
