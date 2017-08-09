# -*- coding: utf-8 -*-

import json
import time
import tornado
import memcache
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic import setting
from system_logic.vo.BaseHandler import BaseHandler
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class BrowseUserListHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('用户列表')

        user_list = [
            {'username':'singlesjjj','telephone':'123456789','sex':'女','birthday':'1993-01-01','balance':'10.0',
             'credit':'100','last_login_ip':'112.10.134.299','last_login_time':'2017-08-08 14:35:02','register_time':'2017-06-22 11:35'},
            {'username': 'lengzhiyuan123', 'telephone': '11111111111', 'sex': '男', 'birthday': '1994-01-01',
             'balance': '11.0', 'credit': '101', 'last_login_ip': '112.10.134.297',
             'last_login_time': '2017-08-06 14:35:02', 'register_time': '2017-06-23 11:35'}

        ]
        self.render('userlist.html', head_info=head_info,user_list=user_list)