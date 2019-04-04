FROM alpine:3.8

MAINTAINER xzr

#设置上下文目录
ENV ALPINE_VERSION=3.8

#系统包 M2Crypto 需要 openssl-dev
ENV PACKAGES="\
  dumb-init \
  bash \
  ca-certificates \
  python2 \
  py-setuptools \
  openssl-dev \
  logrotate   \
"

#编译环境包
ENV BUILD_PACKAGES="\
  build-base \
  linux-headers \
  libc6-compat \
  python2-dev \
  gcc swig tinyxml-dev musl-dev libxslt-dev \
"

WORKDIR /

ADD pip.conf /etc/pip.conf
ADD requirements.txt /requirements.txt

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
  #安装python包,这里不能单独RUN,需要系统dev包
  && pip install --no-cache-dir -r requirements.txt  \
  && apk del --no-cache $BUILD_PACKAGES \
  && rm -rf /var/cache/apk/* \
  && rm -rf /root/.cache \
  && rm -rf /tmp/* \
  && crond

ENTRYPOINT sh


