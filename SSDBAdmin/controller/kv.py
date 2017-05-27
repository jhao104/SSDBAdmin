#!/usr/bin/env python
from SSDBAdmin import app


@app.route('/kv')
def get():
    return 'kv'
