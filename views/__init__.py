# coding:utf-8


import sys, os, time, datetime, uuid
import tornado.escape
import tornado.web
from settings import DEBUG
from base.session import Session
from base.log import Logger
from base.view import BaseHandler
from urls import router
import logging



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
