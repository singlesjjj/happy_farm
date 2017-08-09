# -*- coding: utf-8 -*-

import json
import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
from  system_logic import setting
from system_logic.bo.object.User import User
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class GetCategoryHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        获取商品分类
        :param args:
        :param kwargs:
        :return:
        '''
        condition = {'1=':1}
        supstring = ' ORDER BY category_id'
        category_info = User().get_category(condition, supstring)
        if category_info == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success'],'category_info':category_info}

        self.write(reMsg)