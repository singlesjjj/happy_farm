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

class UserLoginHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        '''
        :param body                     传参
            :param username             用户名
            :param passwd               密码
            :param login_ip             登录ip
        :return:
        :param reMsg                    返回信息
            :param ret                  返回码 -1连接失败， 0账号密码错误， 1登录成功
            :param session
                :param session_id       session号
                :param verify_code      session验证码
        '''
        login_info = json.loads(self.request.body)
        login_info = _decode_dict(login_info)
        u = User()
        result = u.login(login_info)
        reMsg = {'ret':0}
        if result == -1:
            reMsg['ret'] = setting.re_code['connect_error']
        elif result == 0:
            reMsg['ret'] = setting.re_code['verify_error']
        else:
            reMsg['ret'] = setting.re_code['success']
            reMsg['session'] = result
        self.write(reMsg)

class ManagerLoginHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        '''
        同上
        :param args:
        :param kwargs:
        :return:
        '''
        login_info = json.loads(self.request.body)
        login_info = _decode_dict(login_info)
        m = Manager()
        result = m.login(login_info)
        reMsg = {'ret': 0}
        if result == -1 or result == 0:
            reMsg['ret'] = result
        else:
            reMsg['ret'] = 1
            reMsg['session'] = result
        self.write(reMsg)
