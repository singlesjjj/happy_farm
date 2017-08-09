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

class WriteCommentHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self, *args, **kwargs):
        '''
        写评论
        :param body
            :param session_info
            :param comment_info
        :return:
        000001                      连接失败
        000000                      成功
        '''
        apply_info = _decode_dict(json.loads(self.request.body))

        result = User().write_comment(apply_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class UserBrowseCommentHanndler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, *args, **kwargs):
        '''
        用户获取评论
        :param body
            :param product_id
        :return:
        000001                      连接错误
        000000                      成功
        '''
        page_number = self.get_argument('page_number')
        product_id = int(self.get_argument('product_id'))
        condition = {'product_id=':product_id, 'is_delete=':0}

        result, count_num = User().get_comment(condition, page_number)
        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success'],'comment_info':result, 'count_num':count_num}

        self.write(reMsg)
