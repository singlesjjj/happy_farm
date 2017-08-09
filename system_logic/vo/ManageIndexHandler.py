# -*- coding: utf-8 -*-

import json
import time
import tornado
import memcache
import tornado.web
import tornado.ioloop
import tornado.gen
from  system_logic import setting
from system_logic.bo.object.Manager import Manager
from system_logic.vo.BaseHandler import BaseHandler
from system_logic.vo.method.DecodeJson import _decode_dict

mc = memcache.Client(['127.0.0.1:11211'])

class BrowseIndexHandle(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('主页')
        real_name = self.get_secure_cookie('loginuser')

        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        #获近10天的取销售量
        sale_quantity_10days, delta_date = Manager().get_sales_quantity(10, current_date, 1)

        #获取近10天的收入
        income_list, date_list = Manager().get_income(1,current_date,10)

        date_list_str = ''
        for item in date_list:
            date_list_str = item[0:4]+item[5:7]+item[8:] +','+date_list_str
        date_list_str = '['+date_list_str[0:len(date_list_str)-1]+']'

        #将参数写入js
        additional_script = 'var sale_list=%s; var delta_date=%d;' \
                            'var income_list=%s;var date_range=10;var date_list=%s'\
                            %(str(sale_quantity_10days), int(delta_date), str(income_list), date_list_str)

        mc.set(real_name, 1, time=1800)
        self.render('index.html', head_info=head_info, additional_script=additional_script)