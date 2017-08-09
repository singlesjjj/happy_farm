# -*- coding: utf-8 -*-
import time
import datetime
#引入md5加密模块
from system_logic.po.EncryptString import EncryptString
#引入生产随机字符串模块
from system_logic.po.ProduceRandomStr import ProduceRandomStr
#引入配置文件
from system_logic import setting

class PeoplePO:

    def __init__(self):
        self.current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def handle_people_info(self, people_login_info):
        '''
        此方法用以分离people_info, 并且补充没有的信息
        :param people_info_input:                 用户信息
            :param username                 用户名
            :param password                 密码
            :param login_ip                 登录ip
        数据结构
        people_info = {'username', 'password', 'login_ip'}

        :return:
        :param people_info
            :param username                 用户名
            ;:param passwd                  密码
        :param login_info                   保存登录日志
            :param login_ip                 登录ip
            :param login_time               登录时间
        :param last_login_info              修改用户表
            :param last_login_ip            最后登录ip
            :param last_login_time          最后登录时间
        数据结构
        people_info = {'user_name', 'password'}
        login_info = {'login_ip','login_time'}
        last_login_info = {'last_login_ip', 'last_login_time'}
        '''
        people_info = {}
        login_info = {}
        last_login_info = {}
        e = EncryptString()

        for key in people_login_info:
            if key != 'login_ip':
                people_info[key+'='] = people_login_info[key]
            else:
                login_info[key] = people_login_info[key]
                last_login_info['last_'+ key] = people_login_info[key]

        people_info['passwd='] = e.encrypt_string(people_info['passwd='])
        login_info['login_time'] = self.current_time
        last_login_info['last_login_time'] = self.current_time

        return people_info, login_info, last_login_info

    def handle_session(self, applicant_type, applicant_id):
        '''
        此方法用以处理seesion信息
        :param applicant_type:              请求者类型，u-用户， m-管理者
        :param applicant_id:                请求者id
        :return:
        :param mc_key                       缓存session键
        :param mc_value                     缓存session值
            :param expire                   session过期时间
            :param verify_code              验证码
        '''
        p = ProduceRandomStr()
        random_str = p.produce_randomStr()
        mc_key = applicant_type + str(applicant_id)
        expire_time = (datetime.datetime.now() + datetime.timedelta(days = setting.session_valid_days))
        mc_value = {'expire':expire_time, 'verify_code':random_str}
        return mc_key, mc_value

    def handle_sendMsg_info(self, msg_info):
        '''
        此方法用以处理消息数据
        :param msg_info:
        :return:
        '''
        msg_info['send_time'] = self.current_time
        return msg_info

    def handle_Msg_list(self, msg_list):
        '''
        用以处理信息id列表
        :param msg_list:
        :return:
        '''
        condition_list = []
        for item in msg_list:
            condition_dict = {'message_id=':item}
            condition_list.append(condition_dict)
        return condition_list

    def hanlde_product_img_info(self, img_info):
        '''
        处理数据库中取出的图片信息
        :param img_info:                    图片信息
        :return:
        '''
        img_info_re = []
        for item in img_info:
            img_info_re.append(item['img_url'])
        return img_info_re

    def handle_product_property(self, property_info):
        property_info_re = []
        for item in property_info:
            temp_dict = {}
            temp_dict['property_name'] = item['property_name']
            temp_dict['property_content'] = item['property_content']
            property_info_re.append(temp_dict)
        return property_info_re