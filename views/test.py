# -*- coding: utf-8 -*-
# @Time    : 2019-03-14 17:59
# @Author  : xzr
# @File    : test.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


from urls import router
from views import BaseHandler


@router.route('^/phone[/]?$')
class phone(BaseHandler):
    def get(self):
        print self.session['asd']
        self.session['asd'] = 3123
        print self.session
        self.render('phone.html', locals())

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
