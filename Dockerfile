FROM xzregg/py-rsa

MAINTAINER xzr

#设置上下文目录
ENV WORKDIR /data/tornado_project
ENV WORKDIRCOPY $WORKDIR-copy


COPY . $WORKDIRCOPY
WORKDIR $WORKDIRCOPY

RUN pip install --no-cache-dir -r requirements.txt  \
  && rm -rf /var/cache/apk/* \
  && rm -rf /root/.cache \
  && rm -rf /tmp/*



#这里使用ENTRYPOINT代替CMD,统一命令
ENTRYPOINT test -f $WORKDIR/gunicornd.sh || cp -rf $WORKDIRCOPY/* $WORKDIR/ ; sh gunicornd.sh start -s
WORKDIR $WORKDIR

#docker run -it -d -v `pwd`:/data/tornado_project  --log-opt max-size=10m --log-opt max-file=3 --name=tornado_project tornado_project /bin/bash


