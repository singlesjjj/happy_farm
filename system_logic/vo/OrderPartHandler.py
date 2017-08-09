# -*- coding: utf-8 -*-

import json
import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic import setting
from system_logic.bo.object.User import User
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class BrwoseOrderHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        '''

        :param session_id
        :param verify_code
        :param page_number
        :param order_status                         订单状态0-未确认,1-已确认,2-取消,3-无效
        :param shipping_status
        :param payment_status
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')
        session_info = {'session_id':session_id, 'verify_code':verify_code}
        page_number = int(self.get_argument('page_number'))

        user_id = int(session_id[1:])
        condition = {'hf_order.user_id = ':user_id}
        arguments = self.request.query_arguments

        if arguments.has_key('order_status'):
            condition['order_status='] = int(arguments['order_status'][0])
        if arguments.has_key('shipping_status'):
            condition['shipping_status='] = int(arguments['shipping_status'][0])
        if arguments.has_key('payment_status'):
            condition['payment_status='] = int(arguments['payment_status'][0])

        result, count = User().browse_order(session_info, condition, page_number)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'order_info':result, 'count':count}

        self.write(reMsg)

