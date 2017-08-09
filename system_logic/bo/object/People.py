# -*- coding: utf-8 -*-

import time
import datetime
#引入高速缓存模块
import memcache
#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine
#引入数据处理模块
from system_logic.po.PeoplePO import PeoplePO
#引入ip查询模块
from system_logic.po.SearchLocationByIP import SearchLocationByIP

from system_logic.bo.object.static_object.Category import Category
from system_logic.bo.object.static_object.Message import Message

class People:

    def __init__(self, table_name=None):
        self.pp = PeoplePO()
        self.table_name = table_name
        self.mc = memcache.Client(['127.0.0.1:11211'])

    def login(self, people_login_info):
        '''
        此方法用以实现允许用户登录
            1.将用户信息和数据库中信息进行比对,注意密码要经过md5加密后再比对
            2.若正确，将此次回话存入缓存，存入登录日志，并返回登录成功和session_id
            3.若错误，则返回登录失败
        :param people_login_info:           用户信息
            :param username                 用户名
            :param passwd                   密码
            :param login_ip                 登录ip
        数据结构
        people_login_info = {'username', 'password', 'login_ip'}

        :return: result
            -1                               连接失败
            0                                验证失败
            else                             验证成功,session
        '''
        people_info, login_info, last_login_info = self.pp.handle_people_info(people_login_info)
        #获取相应的账号信息
        de = DataBaseEngine(self.table_name)
        operate_type = 'select'
        account_info = de.operate_database(operate_type=operate_type,operate_condition=people_info)

        #如果连接失败或验证失败，返回相应信息
        if account_info == -1:
            return account_info
        elif len(account_info) == 0:
            return 0

        #验证成功，创建session,用14位随机字符串+表名第一个字母+登录者id作为key，value为字典
        #数据结构
        #session = {'random_str':{'expire':'0000-00-00'}}
        applicant_type = self.table_name[0]
        if account_info[0].has_key('user_id'):
            applicant_id = account_info[0]['user_id']
            login_info['user_id'] = applicant_id
        else:
            applicant_id = account_info[0]['manager_id']
            login_info['manager_id'] = applicant_id
        mc_key, mc_value = self.pp.handle_session(applicant_type, applicant_id)
        self.mc.set(mc_key, mc_value)

        #将用户登录信息更新入用户表
        de = DataBaseEngine(self.table_name)
        operate_type = 'update'
        result = de.operate_database(operate_type=operate_type, operate_item=last_login_info, operate_condition=people_info)

        #将用户登录信息写入登录日志表
        table_log = 'login_log_' + self.table_name
        de = DataBaseEngine(table_log)
        location_info = SearchLocationByIP().search_location(login_info['login_ip'])
        login_info['country'] = location_info['country']
        login_info['province'] = location_info['province']
        login_info['city'] = location_info['city']
        operate_type = 'insert'
        result = de.operate_database(operate_type=operate_type, operate_item=login_info)

        #返回session_id
        session = {'session_id':mc_key, 'verify_code':mc_value['verify_code']}
        return session

    def send_message(self, msg_info):
        '''
        此方法用以实现允许人发送消息
        :param msg_info:                        消息数据
            :param sender_id                    发送者id
            :param reciver_id                   接收者id
            :param content                      消息内容
            :param message_type_id              消息类型id
        :return:
            -1                                   连接失败
            else                                 发送成功
        '''
        msg_info = self.pp.handle_sendMsg_info(msg_info)
        de = DataBaseEngine('hf_message')
        operate_type = 'insert'
        result = de.operate_database(operate_type=operate_type, operate_item=msg_info)
        return result

    def mark_messageReaded(self, message_id_list):
        '''
        此方法用以实现用户标记信息已读
        :param message_id_list:             信息id列表
        :return:
        '''
        condition_list = self.pp.handle_Msg_list(message_id_list)
        update_item = {'is_read':1, 'read_time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}
        m = Message()
        result = 1
        for item in condition_list:
            result = m.update_message(update_item, item)
        return result

    def delete_message(self, message_id_list):
        '''
        此方法用以删除信息
        :param message_id_list:
        :return:
        '''
        condition_list = self.pp.handle_Msg_list(message_id_list)
        result = 1
        update_item = {'is_delete':1}
        m = Message()
        for item in condition_list:
            result = m.update_message(update_item, item)
        return result

    def browse_product(self, condition, page_number, each_page_products=12, supstring=None):
        '''
        此方法用以允许用户获取商品信息
        :param condition:                                   条件
        :param each_page_products:                          每页商品数
        :param page_number:                                 请求页数
        :return:
        '''
        page_number = int(page_number)
        each_page_products = int(each_page_products)
        if len(condition) == 0:
            condition = {'1=':1}
        product_start = (page_number-1)*each_page_products

        if supstring != None:
            supstring = 'ORDER BY %s add_time DESC LIMIT %d, %d'%(supstring, product_start, each_page_products)
        else:
            supstring = ' ORDER BY is_hot DESC, add_time DESC LIMIT %d, %d'%(product_start, each_page_products)

        table_name = [
            {'hf_product-hf_product_normal':'product_id'},
            {'hf_product-hf_product_subscription':'product_id'}
        ]

        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        return result

    def browse_product_by_category(self, condition, page_number, each_page_products=12, supstring=None):
        '''
        此方法用于通过分类查询商品
        :param condition:                       同上
        :param page_number:
        :param each_page_products:
        :return:
        '''
        page_number = int(page_number)
        each_page_products = int(each_page_products)
        product_start = (page_number - 1) * each_page_products
        if supstring != None:
            supstring = 'ORDER BY %s add_time DESC LIMIT %d, %d'%(supstring, product_start, each_page_products)
        else:
            supstring = ' ORDER BY is_hot DESC, add_time DESC LIMIT %d, %d'%(product_start, each_page_products)

        table_name = [
            {'hf_product-hf_product_category':'product_id'},
            {'hf_product-hf_product_normal': 'product_id'},
            {'hf_product-hf_product_subscription': 'product_id'}
        ]

        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        return result

    def get_product_imgs(self, condition):
        '''
        此方法用以获取对应商品的图片
        :param condition:                   筛选条件
        :return:
        :param urls_info                    地址信息
            :param img_url                  图片地址
        '''
        de = DataBaseEngine('hf_product_gallery')
        operate_type = 'select'
        supstring = 'ORDER BY sequence_num'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        if result == -1 or len(result) == 0:
            return result
        img_info = self.pp.hanlde_product_img_info(result)
        return img_info

    def get_product_property(self, condition):
        '''
        此方法用以获取对应商品的特性
        :param condition:                   筛选条件
        :return:
        :param property_info                特性信息
            :param property_name            特性名字
            :param property_content         特性内容
        '''
        de = DataBaseEngine('hf_product_property')
        operate_type = 'select'
        supstring = 'ORDER BY property_id'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        if result == -1 or len(result) == 0:
            return result
        property_info = self.pp.handle_product_property(result)
        return property_info

    def get_comments(self, condition, page_number):
        '''
        用以获取商品评论
        :param condition:
        :return:
        '''


        comment_start = (int(page_number) - 1) * 10
        table_name = [
            {'hf_comment-hf_user':'user_id'}
        ]

        supstring = ' ORDER BY comment_time DESC LIMIT %d, 10'%(comment_start)
        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)

        if int(page_number) == 1:
            de = DataBaseEngine('hf_comment')
            operate_type = 'select'
            select_item = {'COUNT(*)':0}
            count_num = de.operate_database(operate_type = operate_type, operate_item=select_item, operate_condition=condition)
            count_num = count_num[0]['COUNT(*)']
        else:
            count_num = -1

        return result, count_num

    def get_category(self, condition, supstring):

        category_info = Category().get_category(condition, supstring)
        return category_info

    def get_address(self, condition):
        '''
        获取用户地址
        :param condition:
        :return:
        '''
        de = DataBaseEngine('hf_address')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        return result

    def get_user(self, condition, supstring = None):
        '''
        此方法用以实现根据条件筛选用户
        :param condition:
        :return:
        '''
        de = DataBaseEngine('hf_user')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        return result

    def browse_article(self, condition, supstring):

        '''
        选取文章列表
        :param condition:
        :param page_number:
        :param supstring:
        :return:
        '''
        de = DataBaseEngine('hf_article')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        return result