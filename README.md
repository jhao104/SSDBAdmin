# SSDBAdmin
SSDB数据库的可视化界面管理工具

## 依赖

* Python 2.x

* Flask

## 安装

下载项目到本地`git clone https://github.com/jhao104/SSDBAdmin.git`

编辑配置文件`SSDBAdmin/setting.py`:
```
servers = [
    {"host": "127.0.0.1",
     "port": 8888},
   ]
```
将`host`和`port`修改成正确值。

安装依赖包:
```pip install -r requirements.txt```

启动:
```python runserver.py```

访问:http://127.0.0.1:5000/ssdbadmin



