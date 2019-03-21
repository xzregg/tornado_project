# -*- coding: utf-8 -*-
# @Time    : 2019-03-14 17:59
# @Author  : xzr
# @Contact : xzregg@gmail.com
# @Desc    : 定义session 类

import sys, os, time
import memcache
import redis
import tornado.web

try:
    import cPickle as Pickle
except:
    import Pickle
from settings import SESSION_ENGINE


class SessionEngine(object):
    cli = None
    address = None
    session_data = {}

    def __init__(self, sid, handler=None):
        self.sid = sid
        self.__class__.session_data.setdefault(sid, {})
        self.session_data = self.__class__.session_data[sid]

    def save_session(self, expire=7200):
        self.__class__.session_data[self.sid] = self.session_data

    def clear_session(self): pass

    def clear(self):
        self.clear_session()


class RedisSessionEngine(SessionEngine):
    rc = None
    address = None

    def __init__(self, sid, handler=None):
        if not self.__class__.rc:
            self.__class__.rc = redis.Redis(*self.address, db=0)
        self.sid = 'session_%s' % sid
        _s = self.rc.get(self.sid)
        self.session_data = Pickle.loads(_s) if _s else {}

    def clear_session(self):
        [self.rc.delete(k) for k in self.rc.keys('session_*')]

    def save_session(self, expire=7200):
        self.rc.set(self.sid, Pickle.dumps(self.session_data))
        self.rc.expire(self.sid, expire)


class MemcacheSessionEngine(SessionEngine):
    mc = None
    address = None

    def __init__(self, sid, handler=None):
        if not self.__class__.mc:
            self.__class__.mc = memcache.Client(self.address)

        self.sid = sid

        self.session_data = self.mc.get(sid) or {}

    def clear_session(self):
        self.mc.flush_all()

    def save_session(self, expire=7200):
        self.mc.set(self.sid, self.session_data, expire)


class CookieSessionEngine(SessionEngine):
    """
    使用tornado Cookie 保存session数据
    """

    def __init__(self, sid, handler=None):
        assert isinstance(handler, tornado.web.RequestHandler)
        self.handler = handler
        self.session_data = {}
        for key, value in self.handler.cookies.items():
            self.session_data[key] = self.handler.get_secure_cookie(key)

    def clear_session(self):
        self.handler.clear_all_cookies()

    def save_session(self, expire=7200):
        for key, value in self.session_data.items():
            if key == 'sid':
                continue
            self.handler.set_secure_cookie(key, str(value), expires=int(time.time()) + expire)



class SessionEngineFactory(object):
    def __init__(self, engine_type=SESSION_ENGINE):
        _type, _address = engine_type.split('://')
        if _type == 'memcache':
            self.se = MemcacheSessionEngine
            self.se.address = [_address]
        elif _type == 'redis':
            _ip, _port = _address.split(':')
            self.se = RedisSessionEngine
            self.se.address = (_ip, int(_port))
        elif _type == 'cookiess':
            self.se = CookieSessionEngine

        print 'USE %s ENGINE !' % _type
        assert self.se, 'Get Session Error'

    def get_session_engine(self):
        return self.se


SessionEngine = SessionEngineFactory(SESSION_ENGINE).get_session_engine()


class Session(dict):
    def __init__(self, sid, handler=None):
        super(Session, self).__init__()
        self.se = SessionEngine(sid, handler)
        self.update(self.se.session_data)

    def __getitem__(self, key):
        if not self.has_key(key):
            return None
        return super(Session, self).__getitem__(key)

    def save(self,expire):

        if cmp(self, self.se.session_data):
            self.se.session_data = self.copy()
            self.se.save_session(expire)


if __name__ == '__main__':
    d1 = dict(zip(range(130), [str(i) * 10 for i in range(100)]))
    d2 = dict(zip(range(150), [str(i) * 1440 for i in range(150)]))

    s = Session('asdddd')
    s['ads'] = d2
    print type(s['ads'])
    print s
    # s.clear()
    s.save()
