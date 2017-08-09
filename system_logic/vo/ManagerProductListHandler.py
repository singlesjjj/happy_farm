# -*- coding: utf-8 -*-

import json
import time
import tornado
import memcache
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic import setting
from system_logic.vo.BaseHandler import BaseHandler
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class BrowseProductListHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('商品列表')

        product_list = [
            {'product_name': 'p_name', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
             'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20'},
            {'product_name': 'p_name1', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
             'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20'},
            {'product_name': 'p_name2', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
             'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20'},
            {'product_name': 'p_name3', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
             'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20'},
            {'product_name': 'p_name4', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
             'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20'},
            {'product_name': 'p_name5', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
             'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20'},
            {'product_name': 'p_name6', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
             'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20'},
            {'product_name': 'p_name7', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
             'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20'},

        ]

        self.render('productlist.html', head_info=head_info,product_list=product_list)