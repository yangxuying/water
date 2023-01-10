FROM python:3.8.9
WORKDIR /YingWater

USER root

RUN  sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  apt-get clean

RUN apt update -y
RUN apt install libgl1-mesa-glx -y
RUN apt install libglib2.0-dev -y

COPY requirements.txt ./

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn gevent

ENV LANG C.UTF-8

EXPOSE 80
