# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     index
   Description :   index view
   Author :        JHao
   date：          2018/8/24
-------------------------------------------------
   Change Activity:
                   2018/8/24: index view
-------------------------------------------------
"""
__author__ = 'JHao'

from SSDBAdmin import app
from SSDBAdmin.setting import DB_CONFIG, VERSION
from SSDBAdmin.model.SSDBClient import getSAServer, SSDBClient
from flask import render_template, request, make_response, redirect, url_for


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error)


# @app.errorhandler(404)
# def not_found_error(error):
#     return redirect(url_for('index'))


@app.route('/ssdbadmin/')
def index():
    host, port = getSAServer(request)
    server_info = SSDBClient(request).serverInfo()
    resp = make_response(render_template('index.html', server_info=server_info))
    resp.set_cookie('SSDBADMINSERVER', '{host}:{port}'.format(host=host, port=port), httponly=True, samesite='Lax')
    return resp


@app.context_processor
def commonParam():
    host, port = getSAServer(request)
    server_list = ['{}:{}'.format(server.get('host'), server.get('port')) for server in DB_CONFIG]
    current_server = '{}:{}'.format(host, port)
    return dict(server_list=server_list, current_server=current_server, version=VERSION)
