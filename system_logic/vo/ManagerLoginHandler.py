# -*- coding: utf-8 -*-

import json
import tornado
import memcache
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic.vo import BaseHandler
from system_logic.bo.object.People import People
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

mc = memcache.Client(['127.0.0.1:11211'])

class ManagerLoginHandler(BaseHandler.BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        login_result = 0
        self.render('login.html', login_result=login_result)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        #获取用户的登录ip，用户名，密码
        client_ip = self.request.remote_ip
        username = str(self.get_argument('username'))
        passwd = str(self.get_argument('passwd'))

        result = Manager().login(username, passwd, client_ip)

        if result == -1 or result == -2:
            self.render('login.html', login_result=result)
        else:
            #设置安全cookie
            self.set_secure_cookie('loginuser', result[0], expires_days=None)
            #设置安全cookie储存管理员头像
            self.set_secure_cookie('profile_img', result[1], expires_days=None)
            # 设置安全cookie储存管理员id
            self.set_secure_cookie('loginuser_id', str(result[2]), expires_days=None)
            #设置缓存
            mc.set(str(result[0]), 1, time=1800)
            self.redirect('/managerindex')

