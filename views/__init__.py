# coding:utf-8


import sys, os, time, datetime, uuid
import tornado.escape
import tornado.web
from settings import DEBUG
from base.session import Session
from base.log import Logger
from urls import router
import logging


class CookieSession(object):
    def __init__(self, handler):
        assert isinstance(handler, tornado.web.RequestHandler)
        self.handler = handler

    def __getitem__(self, key):
        return self.handler.get_secure_cookie(key)

    def __setitem__(self, key, value):
        self.handler.set_secure_cookie(key, str(value))

    def clear(self):
        self.handler.clear_all_cookies()

    def save(self):
        pass


class BaseHandler(tornado.web.RequestHandler):
    escape = tornado.escape

    def render(selfb, template_name, __d={}, **kwargs):
        __d = __d or kwargs
        __d.pop('self', 0)
        super(BaseHandler, selfb).render(template_name, **__d)

    def get_session_id(self):
        sid = self.get_secure_cookie('sid')
        if not sid:
            sid = uuid.uuid4().get_hex()
            self.set_secure_cookie('sid', sid)

        return sid

    def initialize(self):
        self._st = time.time()
        self.session = CookieSession(self)  # Session(self.get_session_id())
        if DEBUG:
            print 'initialize' + '-' * 40
            # print self.cookies
            print self.request
        # print self._headers

    def prepare(self, *args, **kwargs):  # 开始都会运行
        pass

    def on_finish(self):  # 结束都会运行

        self.session.save()


@router.route('^/')
class index(BaseHandler):
    def get(self):
        self.write('index')


@router.route('^/test/(?P<id>.*)')
class test(BaseHandler):
    def get(self, id):
        L = Logger('test', 'test')
        L.info('asdasdasd')
        self.url = '----------'
        self.write('123')
        self.write('%f' % self.request.request_time())
        self.write('<br>%f[%s]' % (self.request.request_time(), self._request_summary()))
        self.render('test.html', locals())

    def on_finish(self):
        super(BaseHandler, self).on_finish()


@router.route('^/route')
class route(BaseHandler):
    def get(self):
        for line in router.Handlers:
            self.write(self.escape.xhtml_escape(str(line)) + '<br>')
