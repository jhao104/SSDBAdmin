from SSDBAdmin import app
from flask import render_template, request, make_response, redirect, url_for

from SSDBAdmin.model.ssdb_admin import get_sa_server
from SSDBAdmin.model.ssdb_admin import SSDBObject
from SSDBAdmin.setting import db_config, PORT


@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error)


@app.context_processor
def pas_server():
    host, port = get_sa_server(request)
    server_list = ['{}:{}'.format(server.get('host'), server.get('port')) for server in db_config]
    current_server = '{}:{}'.format(host, port)
    return dict(server_list=server_list, current_server=current_server)


@app.route('/ssdbadmin/')
def index():
    host, port = get_sa_server(request)
    ssdb_object = SSDBObject(request)
    server_info = ssdb_object.server_info()
    resp = make_response(render_template('index.html', server_info=server_info))
    resp.set_cookie('SSDBADMINSERVER', '{host}:{port}'.format(host=host, port=port))
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
