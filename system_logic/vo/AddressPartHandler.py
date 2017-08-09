# -*- coding: utf-8 -*-

import json
import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic import setting
from system_logic.bo.object.User import User
from system_logic.bo.object.People import People
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class BrowseAddressUser(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        获取地址信息
        :param session_id                   session号
        :param verify_code                  验证码
        :return:
        '''

        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')

        session_info = {'session_id':session_id, 'verify_code':verify_code}

        address_info = User().get_address(session_info)

        if address_info == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        elif address_info == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'address_info':address_info}

        self.write(reMsg)

class AddAddress(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        '''
        添加地址
        :param body
            :param session_info
            :param address_info
                :param country              国家
                :param province             省份
                :param city                 城市
                :param district             区县
                :param address_detail       地址详细
                :param zipcode              邮编
                :param contact_name         联系人名字
                :param contact_number       联系电话
                :param email                邮箱（可选）
        数据结构:
        {session_info:{session_id, verify_code}, address_info:{country, province, city, district, address_detail...}}
        :return:
        '''
        apply_info = json.loads(self.request.body)

        result = User().add_address(apply_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        elif result == -3:
            reMsg = {'ret':setting.re_code['limit_exceeded']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class DeleteAddress(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, *args, **kwargs):
        '''
        删除地址
        :param session_id
        :param verify_code
        :param address_id
        :return:
        '''

        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')
        address_id = self.get_argument('address_id')

        apply_info = {
            'session_info':{'session_id':session_id, 'verify_code':verify_code},
            'address_info':{'address_id':address_id}
        }

        result = User().delete_address(apply_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)