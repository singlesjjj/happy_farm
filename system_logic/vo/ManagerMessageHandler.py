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
from system_logic.po.WebMessagePO import WebMessagePO
from system_logic.vo.method.DecodeJson import _decode_dict

class BrowseManagerMessageHanlder(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        real_name = self.get_secure_cookie('loginuser')
        manager_id = int(self.get_secure_cookie('loginuser_id'))

        head_info = self.get_head_info('消息列表')

        condition = {}
        box_type = 0

        try:
            condition['message_id='] = int(self.get_argument('message_id'))
        except:
            box_type = int(self.get_argument('box_type'))
        try:
            condition['is_read='] = int(self.get_argument('is_read'))
        except:
            pass
        try:
            page_number = int(self.get_argument('page_number'))
        except:
            page_number = 1

        condition, title_name = WebMessagePO().handle_input_condition(box_type,condition,manager_id)

        box_li_id = 'box_li_'+str(box_type)
        manager_info = {'real_name':real_name, 'img_url':head_info['profile_img']}

        message_list = []

        self.render('message.html', head_info=head_info, message_list=message_list,
                    box_li_id=box_li_id,manager_info=manager_info, title_name=title_name)