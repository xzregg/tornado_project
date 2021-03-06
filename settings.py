# -*- coding: utf-8 -*-
# @Time    : 2019-03-14 17:59
# @Author  : xzr
# @Contact : xzregg@gmail.com
# @Desc    : 项目配置

import sys
import os

__od = os.path.dirname

SESSION_ENGINE = 'memcache://127.0.0.1:11211'
# SESSION_ENGINE='redis://127.0.0.1:1111'
SESSION_EXPIRE_TIME = 7200

# 开启debug模式自动重启
DEBUG = False

PROJECT_ROOT = __od(os.path.abspath(__file__))

SETTINGS = {
        'debug'        : DEBUG,
        'template_path': os.path.join(__od(__file__), "templates"),
        'static_path'  : os.path.join(__od(__file__), "static"),
        'cookie_secret': '23123123',
        "gzip"         : True,
}

from environment import *
