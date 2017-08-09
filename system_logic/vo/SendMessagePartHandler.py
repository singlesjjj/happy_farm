# -*- coding: utf-8 -*-

import json
import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
import types
from system_logic import setting
from system_logic.bo.object.People import People
from system_logic.bo.object.User import User
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class SendVerifyMessagePartHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        :param body
            :param telephone            电话号码
            :param msg_type             消息类型，1-注册时发送，2-修改电话时发送
        :return:
        :param reMsg                    返回信息
            :param ret                  -1失败，1成功
        '''
        telephone = str(self.get_argument('telephone'))
        msg_type = self.get_argument('msg_type')
        if msg_type ==  '1':
            template_id = setting.template_id
        elif msg_type == '2':
            template_id = setting.template_id_notify
        else:
            reMsg = {'ret':setting.re_code['parameter_error']}
            self.write(reMsg)
            return
        u = User()
        result = u.get_messageVerifyCode(telephone, template_id)
        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}
        self.write(reMsg)

class ChangeTelePhoneHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, *args, **kwargs):

        '''

        :param user_id                      用户id
        :return:
        '''

        session_id = self.get_argument('session_id')
        user_id = int(session_id[1:])
        condition = {'user_id=':user_id}

        user_info = People().get_user(condition)

        if user_info == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
            self.write(reMsg)
            return
        elif user_info == -2:
            reMsg = {'ret':setting.re_code['session_error']}
            self.write(reMsg)
            return

        telephone = user_info[0]['telephone']
        result = User().get_messageVerifyCode(telephone, 2)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}
        self.write(reMsg)
