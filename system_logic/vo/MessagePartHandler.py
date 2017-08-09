# -*- coding: utf-8 -*-

import json
import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
import types
from system_logic import setting
from system_logic.bo.object.User import User
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class UserSendMsgToManagerHanlder(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        '''
        用户留言给管理员
        :param body
            :param session_info
            :param msg_info
                :param content
        数据结构
        {session_info:{session_id, verify_code}, msg_info:{content}}
        :return:
        '''

        apply_info = _decode_dict(json.loads(self.request.body))

        result = User().send_message_to_manager(apply_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class GetNewMessageCountHanlder(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        获取此用户的未提示消息数量
        :param session_id
        :param verify_code
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')

        session_info = {'session_id':session_id, 'verify_code':verify_code}

        result = User().get_new_message_count(session_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'count':result}

        self.write(reMsg)

class BrowseMessageHanlder(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        获取此用户对应条件的信息
        :param page_number                      请求页数
        :param session_id
        :param verify_code
        :param is_read                          是否阅读0-未读， 1-已读（可选）
        :return:
        '''
        session_id = self.get_argument('session_id')
        user_id = int(session_id[1:])
        verify_code = self.get_argument('verify_code')
        session_info = {'session_id': session_id, 'verify_code': verify_code}
        condition = {'receiver_id=': user_id, 'message_type_id=': 2, 'is_delete=': 0}
        try:
            page_number = int(self.get_argument('page_number'))
        except:
            page_number = 1
        try:
            condition['is_read='] = self.get_argument('is_read')
        except:
            pass
        try:
            condition['message_id='] = self.get_argument('message_id')
        except:
            pass
        try:
            condition['is_alert='] = self.get_argument('is_alert')
        except:
            pass

        result, count = User().browse_message(session_info, condition, page_number)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'msg_info':result, 'count':count}

        self.write(reMsg)

class DeleteMessageHanlder(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        '''
        删除信息
        :param session_id
        :param verify_code
        :param message_id                         需删除的消息id，如果有多个，用逗号分开，如 1,2,3
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')
        session_info = {'session_id': session_id, 'verify_code': verify_code}
        message_id_str = self.get_argument('message_id')

        result = User().delete_message(session_info, message_id_str)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret':setting.re_code['session_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class MarkMessageReadedHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        标记信息已读
        :param session_id
        :param verify_code
        :param messge_id                         需删除的消息id，如果有多个，用逗号分开，如 1,2,3
        :return:
        '''
        session_id = self.get_argument('session_id')
        verify_code = self.get_argument('verify_code')
        session_info = {'session_id': session_id, 'verify_code': verify_code}
        message_id_str = self.get_argument('message_id')

        result = User().mark_message_readed(session_info, message_id_str)

        if result == -1:
            reMsg = {'ret': setting.re_code['connect_error']}
        elif result == -2:
            reMsg = {'ret': setting.re_code['session_error']}
        else:
            reMsg = {'ret': setting.re_code['success']}

        self.write(reMsg)
