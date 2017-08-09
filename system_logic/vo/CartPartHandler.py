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

class BrowseCart(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        浏览用户购物车
        :param body:
            :param session_id                       session号
            :param verify_code                      验证码
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')

        session_info = {'session_id':session_id, 'verify_code':verify_code}

        product_info = User().browse_cart(session_info)

        if product_info == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif product_info == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success'],'product_info':product_info}

        self.write(reMsg)

class AddProductToCart(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        添加商品至购物车
        :param body
            :param session_id
            :param verify_code
            :param product_id
            :param product_quantity
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')
        product_id = self.get_argument('product_id')
        product_quantity = self.get_argument('product_quantity')

        session_info = {'session_id': session_id, 'verify_code': verify_code}
        product_info = {'product_id':product_id, 'product_quantity':product_quantity}

        apply_info = {'session_info':session_info, 'product_info':product_info}

        result = User().add_product_to_cart(apply_info)

        if result == -1:
            reMsg = {'ret': setting.re_code['connect_error']}
        elif result == -2:
            reMsg={'ret': setting.re_code['session_error']}
        else:
            reMsg = {'ret': setting.re_code['success']}

        self.write(reMsg)

class ChangeCartAmount(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''

        :param args:
        :param kwargs:
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')
        product_id = self.get_argument('product_id')
        product_quantity = self.get_argument('product_quantity')

        session_info = {'session_id':session_id,'verify_code':verify_code}
        product_info = {'product_id':product_id, 'product_quantity':product_quantity}

        apply_info = {'session_info':session_info, 'product_info':product_info}

        result = User().change_cart(apply_info)

        if result == -1:
            reMsg = {'ret': setting.re_code['connect_error']}
        elif result == -2:
            reMsg={'ret': setting.re_code['session_error']}
        else:
            reMsg = {'ret': setting.re_code['success']}

        self.write(reMsg)

class DeleteCart(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''

        :param args:
        :param kwargs:
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')
        product_id = self.get_argument('product_id')

        session_info = {'session_id': session_id, 'verify_code': verify_code}
        product_info = {'product_id': product_id, 'is_delete': 1}

        apply_info = {'session_info': session_info, 'product_info': product_info}

        result = User().change_cart(apply_info)

        if result == -1:
            reMsg = {'ret': setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret': setting.re_code['session_error']}
        else:
            reMsg = {'ret': setting.re_code['success']}

        self.write(reMsg)