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

class BrowseUserInfoUserHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        '''
        获取用户信息
        :param session_id
        :param verify_code
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')

        session_info = {'session_id':session_id, 'verify_code':verify_code}

        result = User().get_user(session_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'user_info':result}

        self.write(reMsg)

class ModifyUserInfoHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        '''
        修改个人信息
        :param body
            :param session_info
            :param user_info
                :param sex                          性别(可选)
                :param birthday                     生日(可选)
        :return:
        '''
        apply_info = _decode_dict(json.loads(self.request.body))

        result = User().modify_user_info(apply_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class UploadProfilePicHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        '''
        上传头像图片
        :param body
            :param session_info
            :param pic_info
                :param base64_str
        :return:
        :param profile_url
        '''
        apply_info = _decode_dict(json.loads(self.request.body))

        result = User().upload_profile_pic(apply_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'profile_url':result}

        self.write(reMsg)

class UpdateUserTelephoneHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        '''

        :param body
            :param session_info
            :param tele_info
                :param old_tele                 旧手机号
                :param new_tele                 新手机号
                :param verify_code              验证码
        数据结构:
        {session_inf:{session_id, verify_code}, tele_info:{old_tele, new_tele, verify_code}}
        :return:
        '''
        apply_info = _decode_dict(json.loads(self.request.body))

        result = User().change_telephone(apply_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        elif result == -3:
            reMsg = {'ret':setting.re_code['verify_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class ChangeUserPasswordHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        '''
        用户修改密码
        :param body
            :param session_info
            :param passwd_info
                :param old_passwd
                :param new_passwod
        数据结构
        {sesion_info:{session_id, verify_code},passwd_info:{old_passwd, new_passwd}}
        :return:
        '''
        apply_info = _decode_dict(json.loads(self.request.body))

        result = User().change_passwd(apply_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        elif result == -3:
            reMsg = {'ret':setting.re_code['verify_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)
