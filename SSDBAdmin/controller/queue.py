#!/usr/bin/env python

from SSDBAdmin import app
from flask import render_template, request, make_response, redirect, url_for

from SSDBAdmin.model.ssdb_admin import SSDBObject


@app.route('/ssdbadmin/queue/')
def queue_list():
    """
    return all queue
    :return:
    """
    ssdb_object = SSDBObject(request)
    queue_list = ssdb_object.queue_list(start='')
    return render_template('queue_list.html', queue_list=queue_list)


@app.route('/ssdbadmin/queue/qpush/', methods=['GET', 'POST'])
def queue_qpush():
    """
    add item to queue
    :return:
    """
    if request.method == 'GET':
        queue_name = request.args.get('n')
        return render_template('queue_qpush.html', queue_name=queue_name)
    else:
        queue_name = request.form.get('queue_name')
        push_type = request.form.get('type')
        item = request.form.get('item')
        ssdb_object = SSDBObject(request)
        ssdb_object.queue_qpush(queue_name, item, push_type)
        return redirect(url_for('queue_list'))


@app.route('/ssdbadmin/queue/qpop/', methods=['GET', 'POST'])
def queue_qpop():
    """
    pop item from queue
    :return:
    """
    if request.method == 'GET':
        queue_name = request.args.get('n')
        return render_template('queue_qpop.html', queue_name=queue_name)
    else:
        queue_name = request.form.get('n')
        pop_type = request.form.get('t')
        number = request.form.get('num')
        ssdb_object = SSDBObject(request)
        ssdb_object.queue_qpop(queue_name, number, pop_type)
        return redirect(url_for('queue_list'))
