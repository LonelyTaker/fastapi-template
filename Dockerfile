#!/bin/bash
FROM python:3.10-bookworm

ENV TZ=Asia/Shanghai

ARG WORKDIR="/usr/local/app"

WORKDIR ${WORKDIR}

COPY requirements.txt .

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y apt-utils net-tools telnet vim \
    && echo "alias ll='ls -alF'" >> /etc/bash.bashrc \
    && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 7866

CMD ["bash"]