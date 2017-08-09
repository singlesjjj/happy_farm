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

class BrowseMessgeDetailHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('消息列表')

        try:
            message_id = int(self.get_argument('message_id'))
        except:
            message_id = None

        manager_info = [
            {'username': 'singlesjjj'}
        ]

        if message_id == 3:
            message_list = [
                {'sender_name': '1234', 'msg_content': 'lallalalkklsdfjklsdf', 'send_time': '2017-05-06',
                 'is_read': 0},
            ]
        self.render('messagedetail.html', head_info = head_info,message_list=message_list,manager_info=manager_info)
