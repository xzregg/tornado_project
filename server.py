# -*- coding: utf-8 -*-
# @Time    : 2019-03-14 17:59
# @Author  : xzr
# @File    : server.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 项目开始布局 https://github.com/bueda/tornado-boilerplate


import time, os, sys
from tornado.options import define, options
import tornado.web
import tornado.httpserver
import logging
from tornado.options import define, options, parse_command_line
import signal
from urls import URLS
from settings import SETTINGS

define("port", default=9009, help="监听的端口", type=int)

application = tornado.web.Application(handlers=URLS, **SETTINGS)


def init_logging():
    tornado.options.parse_command_line()
    from tornado.log import LogFormatter
    access_log = logging.getLogger()
    datefmt = '[%Y-%m-%d %H:%M:%S %z]'
    fmt = '%(asctime)s [%(levelname)s %(name)s pid:%(process)d port:{port} %(filename)s:%(lineno)d] %(message)s'.format(
            port=options.port or '')
    formatter = LogFormatter(color=True, fmt=fmt, datefmt=datefmt)
    access_log.handlers[0].setFormatter(formatter)


def kill_server(sig, frame):
    logging.info('Caught signal: %s stop server(%s)' % (sig, options.port))
    tornado.ioloop.IOLoop.instance().stop()


def register_signal():
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    signal.signal(signal.SIGINT, kill_server)
    signal.signal(signal.SIGQUIT, kill_server)
    # signal.signal(signal.SIGTERM, kill_server)
    signal.signal(signal.SIGHUP, kill_server)


def run_server():
    server = tornado.httpserver.HTTPServer(application, xheaders=True, no_keep_alive=False)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


register_signal()
init_logging()

if __name__ == '__main__':
    print 'start server http://0.0.0.0:%s/' % options.port
    run_server()
