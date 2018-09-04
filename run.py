# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     run
   Description :   SSDB Admin Launcher
   Author :        JHao
   date：          2018/8/24
-------------------------------------------------
   Change Activity:
                   2018/8/24: SSDB Admin Launcher
-------------------------------------------------
"""
__author__ = 'JHao'

from SSDBAdmin import app


def run():
    service_config = app.config.get("SERVICE_CONFIG")
    host = service_config.get("host")
    port = service_config.get("port")
    debug = service_config.get("debug")

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run()
