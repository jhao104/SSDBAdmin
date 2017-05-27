#!/usr/bin/env python

from SSDBAdmin import app


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
