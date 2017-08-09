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

class BrowseArticleListHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        获取文章列表
        :param page_number                      页数
        :return:
        '''
        page_number = self.get_argument('page_number')
        condition = {'is_delete=':0}

        result = User().browse_article_list(condition, page_number)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'article_info':result}

        self.write(reMsg)

class BrowseArticleDetailHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, *args, **kwargs):
        '''
        获取文章详细信息
        :param article_id
        :return:
        '''
        article_id = int(self.get_argument('article_id'))
        condition = {'is_delete=':0, 'article_id=':article_id}
        result = User().browse_article_detail(condition)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'article_info':result}

        self.write(reMsg)
