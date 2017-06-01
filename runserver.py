#!/usr/bin/env python

from SSDBAdmin import app
from flask import render_template, request, make_response

from SSDBAdmin.model.ssdb_admin import get_sa_server
from SSDBAdmin.setting import servers


@app.context_processor
def pas_server():
    host, port = get_sa_server(request)
    server_list = ['{}:{}'.format(server.get('host'), server.get('port')) for server in servers]
    current_server = '{}:{}'.format(host, port)
    return dict(server_list=server_list, current_server=current_server)


@app.route('/ssdbadmin/')
def index():
    host, port = get_sa_server(request)
    resp = make_response(render_template('index.html'))
    resp.set_cookie('SSDBADMINSERVER', '{host}:{port}'.format(host=host, port=port))
    return resp


if __name__ == '__main__':
    app.run()
