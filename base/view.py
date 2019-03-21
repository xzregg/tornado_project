# -*- coding: utf-8 -*-
# @Time    : 2019-03-20 09:32
# @Author  : xzr
# @File    : view
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 

import sys, os, time, datetime, uuid
import tornado.escape
import tornado.web
from settings import DEBUG
from base.session import Session
from base.log import Logger
from urls import router
import logging
from settings import SESSION_ENGINE,SESSION_EXPIRE_TIME


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
        self.session = Session(self.get_session_id(), self)

    def prepare(self, *args, **kwargs):
        """
        开始都会运行
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def finish(self, *args, **kwargs):
        self.session.save(SESSION_EXPIRE_TIME)
        super(BaseHandler, self).finish(*args, **kwargs)

    def on_finish(self):
        """
        结束都会运行

        :return:
        """
        pass
