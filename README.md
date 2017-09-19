SSDBAdmin
=======
[![Build Status](https://travis-ci.org/jhao104/SSDBAdmin.svg?branch=master)](https://travis-ci.org/jhao104/SSDBAdmin) ![py27](https://camo.githubusercontent.com/392a32588691a8418368a51ff33a12d41f11f0a9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d322e372d6666363962342e737667) [![Requirements Status](https://requires.io/github/jhao104/SSDBAdmin/requirements.svg?branch=master)](https://requires.io/github/jhao104/SSDBAdmin/requirements/?branch=master)

SSDB数据库的可视化界面管理工具


## 功能
    提供SSDB数据的hash/zset/kv/queue等数据结构的增删改查等功能

## 依赖

* Python 2.x

* Flask

## 安装

下载项目到本地`git clone https://github.com/jhao104/SSDBAdmin.git`

编辑配置文件`SSDBAdmin/setting.py`:
```
# SSDB config
db_config = [
    {"host": "127.0.0.1",
     "port": 8888},
   ]
PORT = 5000  # server config
```
将`host`和`port`修改成正确值。

安装依赖包:
```pip install -r requirements.txt```

启动:
```python runserver.py```

访问:http://127.0.0.1:5000/ssdbadmin

## Release notes

* 0.2

  * change ssdb driver; use python-redis.py replace ssdb-py。

* 0.1

  * First release of SSDBAdmin;
  * `List`/`Hashmap`/`Set`/`KeyValue` operate;

## Screenshots

![](./SSDBAdmin/static/img/index.png)

![](./SSDBAdmin/static/img/queue.png)
