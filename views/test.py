# -*- coding: utf-8 -*-
# @Time    : 2019-03-14 17:59
# @Author  : xzr
# @File    : test.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


import sys, os, time, datetime, uuid
import tornado.escape
import tornado.web
from views import BaseHandler
from settings import DEBUG
from base.session import Session
from base.log import Logger
from urls import router


@router.route('^/phone[/]?$')
class phone(BaseHandler):
    def get(self):
        self.render('phone.html', locals())

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
