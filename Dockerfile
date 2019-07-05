FROM python:3.6

MAINTAINER jhao104 "j_hao104@163.com"

ENV TZ Asia/Shanghai

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

COPY . /


ENTRYPOINT [ "python", "run.py"]