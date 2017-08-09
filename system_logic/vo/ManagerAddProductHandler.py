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
from system_logic.po.PageAddProductPO import PageAddProductPO
from system_logic.vo.method.DecodeJson import _decode_dict

class AddProductHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        渲染添加商品页面
        :param args:
        :param kwargs:
        :return:
        '''
        #判断用户是否登录
        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('添加商品')
        product_type_list = Manager().get_product_type()
        category_list = Manager().get_category({'1=':1},'ORDER BY category_id ASC')
        category_list = PageAddProductPO().handle_category_list(category_list)

        self.render('addproduct.html', head_info=head_info, product_type_list=product_type_list,
                    category_list=category_list)

