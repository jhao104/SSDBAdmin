from flask import Flask

app = Flask(__name__)
app.config.from_object('SSDBAdmin.setting')

from SSDBAdmin.apps import index
from SSDBAdmin.apps import kv
from SSDBAdmin.apps import hash
from SSDBAdmin.apps import zset
from SSDBAdmin.apps import queue
