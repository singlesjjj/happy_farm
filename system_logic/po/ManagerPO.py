# -*- coding: utf-8 -*-

import random
import time
import datetime
from system_logic.po.ProduceRandomStr import ProduceRandomStr

class ManagerPO:

    def __init__(self):
        self.current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def handle_login_info(self, manager_id, location_info):

        location_info['manager_id'] = manager_id
        location_info['login_time'] = self.current_time
        return location_info, self.current_time

    def hanlde_registerInfo(self, apply_info):
        '''
        处理注册管理员用户的输入信息
        :param apply_info:                  请求信息
            :param session_info             session信息
                :param session_id           session号
                :param verify_code          验证码
            :param register_info            注册信息
                :param username             用户名
                :param passwd               密码
                :param real_name            真实姓名
                :param telephone            电话号码
                :param authority            权限
                :param manager_menu         拥有菜单

        :return:
            session_info                     session信息
            add_manager_info                 管理员信息
            manager_menu_info                管理员菜单权限信息
        '''
        session_info = apply_info['session_info']
        add_manager_info = {}
        manager_menu_info = []
        for key in apply_info['register_info']:
            if key != 'manager_menu':
                add_manager_info[key] = apply_info['register_info'][key]
            else:
                manager_menu_info = apply_info['register_info'][key]
        add_manager_info['add_time'] = self.current_time
        return session_info, add_manager_info, manager_menu_info

    def handle_managerMenu(self, manager_id, manager_menu):
        '''
        此方法用以处理管理员和菜单权限的数据
        :param manager_id:                  管理员id
        :param manager_menu:                管理员菜单权限列表
        :return:
        :param manager_menu_list            管理员菜单权限插入列表
        数据结构
        '''
        manager_menu_list=[]
        for item in manager_menu:
            temp_dict = {'manager_id':manager_id, 'menu_id':item}
            manager_menu_list.append(temp_dict)
        return manager_menu_list

    def handle_product_info(self, apply_info):
        '''

        :param apply_info:                  内容同Manager类中的add_product方法的apply_info
        :return:
        :param session_info                 session信息
        :param product_basic_info           商品基本信息
        :param prodcut_sub_info             商品补充信息
        :param product_attribute_info       商品属性信息
        :param product_act_log_info         商品操作日志信息
        :param product_gallery_info         商品图片信息
        '''
        session_info = apply_info['session_info']
        product_basic_info = apply_info['product_info']['basic_info']
        product_sub_info = apply_info['product_info']['sub_info']
        product_category_info = apply_info['product_info']['product_category_info']
        product_gallery_info = apply_info['product_info']['product_gallery_info']
        product_property_info = apply_info['product_info']['product_property_info']

        #生成商品编号 xxxxxx-xx-xxxx-xxxx
        # 前6位是日期，7-8位是商品类型，00普通商品，01认领商品, 9-12位是添加者id，13到16位是随机数
        first_part = time.strftime('%Y%m%d', time.localtime(time.time()))[2:]
        second_part = '0'+ str(product_basic_info['product_type'])
        manager_id = session_info['session_id'][1:]
        thrid_part = manager_id
        for i in range(len(manager_id),4):
            thrid_part = '0' + thrid_part
        fouth_part = ProduceRandomStr().product_randomInt()
        product_sn = first_part + second_part + thrid_part + fouth_part
        product_basic_info['product_sn'] = product_sn

        product_basic_info['add_time'] = self.current_time

        product_act_log_info = {'manager_id':manager_id, 'act_type_id':1, 'act_time':self.current_time}

        return session_info, product_basic_info, product_sub_info, product_category_info, \
               product_act_log_info, product_gallery_info, product_property_info

    def handle_product_category_info(self, product_id, category):
        product_category_list = []
        for item in category:
            temp_dict = {'product_id': product_id, 'category_id': item}
            product_category_list.append(temp_dict)
        return product_category_list

    def handle_product_gallery_info(self, product_id, gallery):
        product_category_list = []
        for item in gallery:
            temp_dict = item
            temp_dict['product_id'] = product_id
            product_category_list.append(temp_dict)
        return product_category_list

    def handle_product_property_info(self, product_id, property):
        product_property_list = []
        for item in property:
            temp_dict = item
            temp_dict['product_id'] = product_id
            product_property_list.append(temp_dict)
        return product_property_list

    def handle_sale_quantity_date(self, right_date, delta_number, get_type):

        date_list = []
        delta_date = 0
        for i in range(0, delta_number):
            if get_type == 1:
                right_datetime = datetime.datetime.strptime(right_date, '%Y-%m-%d').date()
                d2 = datetime.date(int(right_date[0:4]), 1, 10)
                delta_date = (right_datetime - d2).days
                datetime_temp = str(right_datetime-datetime.timedelta(days=i))
                date_list.append(datetime_temp)
            elif get_type == 2:
                month_number = int(right_date[5:7])
                month_number_1 = month_number-i
                if month_number_1 > 0:
                    if len(str(month_number_1)) == 1:
                        month_temp = '0'+str(month_number_1)
                    else:
                        month_temp = str(month_number_1)
                    datetime_temp = right_date[0:4] + '-' + month_temp
                    date_list.append(datetime_temp)
            else:
                year_number = int(right_date[0:4])
                year_num = year_number - i
                if year_num > 0:
                    if len(str(year_num)) == 1:
                        _temp = '000' + str(year_num)
                    elif len(str(year_num)) == 2:
                        _temp = '00' + str(year_num)
                    elif len(str(year_num)) == 3:
                        _temp = '0' + str(year_num)
                    else:
                        _temp = str(year_num)
                    datetime_temp = _temp
                    date_list.append(datetime_temp)

        return date_list,delta_date

    def handle_income_condition(self, product_type, date_item):

        if product_type == -1:
            condition = [
                {'(payment_date IS NULL': {'value': '', 'symbol': 'AND'}},
                {'create_time LIKE': {'value': date_item + '%%', 'symbol': ') OR'}},
                {'payment_date LIKE': {'value': date_item + '%%', 'symbol': ''}}
            ]
        else:
            condition = [
                {'((payment_date IS NULL': {'value': '', 'symbol': 'AND'}},
                {'create_time LIKE': {'value': date_item + '%%', 'symbol': ') OR'}},
                {'payment_date LIKE': {'value': date_item + '%%', 'symbol': ') AND'}},
                {'product_type=': {'value':product_type, 'symbol':''}}
            ]
        return condition

    def handle_income(self, info_list):
        subtotal = 0
        for item in info_list:
            if item['product_type'] == 0 or item['product_type'] == 2:
                subtotal = subtotal + float(item['order_subtotal'])
            else:
                subtotal = subtotal + float(item['amount'])
        return subtotal
