# -*- coding: utf-8 -*-

import json
import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
import types
from system_logic.bo.object.User import User
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class UserRegisterHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        '''
        @:param body
            :param username                 用户名
            :param passwd                   密码
            :param verify_code              手机验证码
            :param telephone                电话
            :param login_ip                 注册时ip
        :return:
        :param reMsg                    返回信息
            :param ret                  返回码 -1连接失败， 0用户名已存在， -2电话已绑定, -3手机验证吗验证失败, 1注册并登录成功
            :param session
                :param session_id       session号
                :param verify_code      session验证码
        '''
        reg_info = _decode_dict(json.loads(self.request.body))
        u = User()
        result = u.register(reg_info)
        reMsg = {'ret':-1}
        if type(result) is types.IntType:
            reMsg['ret'] = result
        else:
            reMsg['ret'] = 1
            reMsg['session'] = result

        self.write(reMsg)

class ManagerRegisterHandler(tornado.web.RequestHandler):

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
        :param reMsg                    返回信息
            :param ret                  返回码 -1连接失败， -2session失效, -3权限不足, -4用户名重复， 1添加成功
        '''
        reg_info = _decode_dict(json.loads(self.request.body))
        m = Manager()
        result = m.register(reg_info)
        reMsg = {}
        if result != -1 and result != -2 and result != -3 and result != -4:
            reMsg['ret'] = 1
        else:
            reMsg['ret'] = result
        self.write(reMsg)


