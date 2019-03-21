FROM alpine:3.8
#设置上下文目录
ENV WORKDIR /data/tornado_project

ENV ALPINE_VERSION=3.8

#系统包 M2Crypto 需要 openssl-dev
ENV PACKAGES="\
  dumb-init \
  bash \
  ca-certificates \
  python2 \
  py-setuptools \
  openssl-dev \
"
#编译环境包
ENV BUILD_PACKAGES="\
  build-base \
  linux-headers \
  libc6-compat \
  python2-dev \
  gcc swig tinyxml-dev musl-dev libxslt-dev \
"

WORKDIR $WORKDIR
COPY . $WORKDIR
ADD pip.conf /etc/pip.conf

RUN echo \
  # 阿里云镜像
  && echo "http://mirrors.aliyun.com/alpine/v$ALPINE_VERSION/releases" > /etc/apk/repositories \
  && echo "http://mirrors.aliyun.com/alpine/v$ALPINE_VERSION/community" >> /etc/apk/repositories \
  && echo "http://mirrors.aliyun.com/alpine/v$ALPINE_VERSION/main" >> /etc/apk/repositories \
  # 安装系统包,requirements所需的编译环境包
  && apk add --no-cache $PACKAGES $BUILD_PACKAGES \
  # make some useful symlinks that are expected to exist
  && if [[ ! -e /usr/bin/python ]];        then ln -sf /usr/bin/python2.7 /usr/bin/python; fi \
  && if [[ ! -e /usr/bin/python-config ]]; then ln -sf /usr/bin/python2.7-config /usr/bin/python-config; fi \
  && if [[ ! -e /usr/bin/easy_install ]];  then ln -sf /usr/bin/easy_install-2.7 /usr/bin/easy_install; fi \
  # Install and upgrade Pip
  && easy_install pip \
  && pip install --upgrade pip \
  && if [[ ! -e /usr/bin/pip ]]; then ln -sf /usr/bin/pip2.7 /usr/bin/pip; fi \
  && mkdir -pv $WORKDIR
  #安装python包
RUN pip install --no-cache-dir -r requirements.txt  \
  #之后删除编译环境包
  && apk del --no-cache $BUILD_PACKAGES \
  && rm -rf /var/cache/apk/* \
  && rm -rf /root/.cache \
  && rm -rf /tmp/*
	
CMD sh gunicornd.sh start -s

#docker run -it -d -v `pwd`:/data/tornado_project  --log-opt max-size=10m --log-opt max-file=3 --name=tornado_project sdk_vs:latest /bin/bash
#docker exec -it tornado_project /bin/bash

