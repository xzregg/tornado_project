# -*- coding: utf-8 -*-
# @Time    : 2019-03-14 17:59
# @Author  : xzr
# @Contact : xzregg@gmail.com
# @Desc    : 这里注册views


from tornado.web import url, StaticFileHandler
from settings import SETTINGS
import router

import views
from views.test import *

URLS = [(r"/static/(.*)", StaticFileHandler, {"path": SETTINGS['static_path']})] + router.Handlers
