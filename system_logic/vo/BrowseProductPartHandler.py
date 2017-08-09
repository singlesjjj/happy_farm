# -*- coding: utf-8 -*-

import json
import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic import setting
from system_logic.bo.object.User import User
from system_logic.bo.object.People import People
from system_logic.po.BrwoseProductInputPO import BrowseProductInputPO
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class UserBrowseProductHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        此方法用以获取商品列表信息
        :param body
            :param page_number                  页数，默认1
            :param product_name                 商品名字，模糊查询(可选)
            :param product_id                   商品id(可选)
            :param product_type                 商品类型0-普通，1-领养(可选)
            :param left_price                   价格区间左值(可选)
            :param right_price                  价格区间又值(可选)
            :param sort_by                      不填，按热门排序，price_a价格升序，price_d价格降序，time时间降序(可选)
        :return:
        :param reMsg                            返回信息
            :param ret                          返回码,000001连接失败,000000成功
            :param product_info                 商品信息
        '''
        arguments = self.request.query_arguments

        if arguments.has_key('category_id'):
            reMsg = {'ret':setting.re_code['parameter_error']}
            self.write(reMsg)
            return

        condition, page_number, each_page_products, supstring = BrowseProductInputPO().handle_browse_product_input(arguments)

        product_info = User().browse_product(condition, page_number, each_page_products, supstring=supstring)
        reMsg = {}
        if product_info==-1:
            reMsg['ret'] = setting.re_code['connect_error']
        else:
            reMsg['ret'] = setting.re_code['success']
            reMsg['product_info'] = product_info

        self.write(reMsg)

class UserBrowserProductCategoryHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        参数同上
        :return:
        :param reMsg                        返回信息
        :param ret                          返回码,000001连接失败,000000成功,000007参数错误
        :param product_info                 商品信息
        '''
        arguments = self.request.query_arguments
        if not arguments.has_key('category_id'):
            reMsg = {'ret':setting.re_code['parameter_error']}
            self.write(reMsg)
            return

        condition, page_number, each_page_products, supstring = BrowseProductInputPO().handle_browse_product_input(arguments)

        product_info = User().browse_product_by_category(condition, page_number, each_page_products, supstring)
        reMsg = {}
        if product_info == -1:
            reMsg['ret'] = setting.re_code['connect_error']
        else:
            reMsg['ret'] = setting.re_code['success']
            reMsg['product_info'] = product_info

        self.write(reMsg)

class GetProductImgHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        用于获取商品图片信息
        :param body
            :param product_id
        :return:
        '''
        product_id = int(self.get_argument('product_id'))
        condition = {'product_id=':product_id,'is_delete=':0}
        img_info =  People().get_product_imgs(condition)
        reMsg = {'ret':setting.re_code['connect_error']}
        if img_info != -1:
            reMsg['ret'] = setting.re_code['success']
            reMsg['img_info'] = img_info
        self.write(reMsg)

class GetProductPropertyHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        用于获取商品特性信息
        :param body
            :param product_id
        :return:
        '''
        product_id = int(self.get_argument('product_id'))
        condition = {'product_id=':product_id, 'is_delete=':0}
        property_info = People().get_product_property(condition)
        reMsg = {'ret': setting.re_code['connect_error']}
        if property_info != -1:
            reMsg['ret'] = setting.re_code['success']
            reMsg['property_info'] = property_info
        self.write(reMsg)

class GetProductCategoryHanlder(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, *args, **kwargs):

        product_id = self.get_argument('product_id')
        result = User().get_product_category({'product_id=':product_id})
        if result == -1:
            reMsg = {'ret':setting.re_code['success'], 'product_category':''}
        else:
            reMsg = {'ret': setting.re_code['success'], 'product_category': result}
        self.write(reMsg)
