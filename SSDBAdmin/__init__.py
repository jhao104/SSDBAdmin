#!/usr/bin/env python
from flask import Flask

app = Flask(__name__)
app.config.from_object('SSDBAdmin.setting')

from SSDBAdmin.controller import kv
from SSDBAdmin.controller import hash
from SSDBAdmin.controller import zset
from SSDBAdmin.controller import queue
