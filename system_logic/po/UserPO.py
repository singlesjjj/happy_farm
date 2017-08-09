# -*- coding: utf-8 -*-

import json
import random
import time
import datetime
import base64
#引入配置文件
from system_logic import setting
#引入md5加密模块
from system_logic.po.EncryptString import EncryptString

class UserPO:

    def __init__(self):
        pass

    def handle_registerInfo(self, register_info):
        '''
        此方法用以从注册信息中获取登录信息,注册信息，用户名，电话
        :param register_info:
        :return:
        '''
        username_dic = {'username=':register_info['username']}
        telephone_dic = {'telephone=':register_info['telephone']}
        verify_code = register_info['verify_code']
        login_info = {
            'username':register_info['username'],
            'passwd':register_info['passwd'],
            'login_ip':register_info['login_ip']
        }
        e = EncryptString()
        reg_info = {
            'username':register_info['username'],
            'passwd':e.encrypt_string(register_info['passwd']),
            'telephone':register_info['telephone'],
            'register_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        }
        return username_dic, telephone_dic, login_info, reg_info, verify_code

    def handle_yunzhixunParas(self, telephone, template_id):
        '''
        此方法用以生成云之讯所需的参数
        :param telephone                    电话号码
        :return:
        :param url                          连接地址
        :param account_sid                  账户id
        :param timestamp                    时间戳
        :param resposeMode                  请求类型
        :param mc_value                     缓存值
        :param body                         请求主体
            :param templateSMS             模板短信信息
                :param appId                应用id
                :param to                   发送至号码
                :param templateId           模板id
                :param param                参数
        '''

        resposeMode = setting.JSON
        code_expire = setting.code_expire
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        #获取签名
        e = EncryptString()
        input_str = setting.account_sid + setting.account_token + timestamp
        signature = e.encrypt_string(input_str).upper()

        #获取6位随机码,并加上过期时间成为参数
        verify_code = str(random.randint(100000,999999))
        param = verify_code + ',' + code_expire
        expire_time = (datetime.datetime.now() + datetime.timedelta(minutes=int(code_expire)))
        mc_value = {'expire':expire_time, 'verify_code': verify_code}
        #完整链接地址
        url = setting.api_url + ':' + setting.port + '/' + setting.soft_version + \
              '/Accounts/' + setting.account_sid + '/Messages/templateSMS?sig='+signature

        #创建请求主体
        body = {
            'templateSMS':{
                'appId':setting.app_id,
                'to':telephone,
                'templateId':template_id,
                'param':param
            }
        }
        body = json.dumps(body)
        return url, setting.account_sid, timestamp, resposeMode, mc_value, body

    def handle_authInfo(self, account_sid, timestamp):
        '''
        此方法用以生产授权信息
        :return: auth                   授权信息
        '''
        auth_str = account_sid + ':' + timestamp
        #auth_str='354fbfb43d1644ddb6d98218210247d8:20170627151218'
        #auth_str='354fbfb43d1644ddb6d98218210247d8:20170627151218'
        auth = base64.encodestring(auth_str).strip()
        return auth

    def createHttpReq(self, req, auth, responseMode, body):
        '''
        此方法用以生成http请求报文
        :return: req                    报文
        '''
        req.add_header('Authorization', auth)
        if responseMode:
            req.add_header('Accept','application/' + responseMode)
            req.add_header('Content-Type', 'application/' + responseMode + ';charset=utf-8')
        if body:
            req.add_header('Content-Length', len(body))
            req.add_data(body)
        return req

    def handle_browse_product_info(self, product_info):
        '''
        此方法用以处理从数据库中取出的商品信息
        :param product_info:                            商品信息
            blabla～太多信息不想写了～
        :return:
        '''
        product_info_re = []
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        for item in product_info:
            temp_dict = {
                'product_id':item['product_id'],
                'product_name':item['product_name'],
                'product_type':item['product_type'],
                'is_hot':item['is_hot'],
                'thumb_img_url':item['thumb_img_url'],
                'brief':item['brief'],
                'description':item['description'],
                'attribute':item['attribute'],
                'unit':item['unit'],
                'stock':item['stock']
            }
            if item['product_type']==0 or item['product_type'] == 2:
                temp_dict['shop_price'] = item['shop_price']
                temp_dict['promote_price'] = ''
                if item['promote_price'] != '' and current_time > item['promote_start_date'] and current_time < item['promote_end_date']:
                    temp_dict['promote_price'] = item['promote_price']
            else:
                temp_dict['first_pay'] = item['first_pay']
                temp_dict['each_month_pay'] = item['each_month_pay']
                temp_dict['need_to_pay_month'] = item['need_to_pay_month']
            product_info_re.append(temp_dict)

        return product_info_re

    def handle_cart_info(self, apply_info):
        '''

        :param apply_info:
        :return:
        '''
        session_info = apply_info['session_info']
        user_id = int(session_info['session_id'][1:])
        product_id = apply_info['product_info']['product_id']
        product_quantity = apply_info['product_info']['product_quantity']
        add_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        condition = {'product_id=':product_id,'user_id=':user_id, 'is_delete=':0}
        cart_info = {'user_id':user_id, 'product_id':product_id,
                     'product_quantity':product_quantity,'add_time':add_time}
        return session_info, condition, cart_info

    def handle_comment_info(self, apply_info):
        '''

        :param apply_info:
        :return:
        :param comment_info
            :param comment_content
            :param user_id
            :param product_id
            :param comment_time
        :param session_info
        '''
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        session_info = apply_info['session_info']
        comment_info = apply_info['comment_info']
        user_id = int(session_info['session_id'][1:])

        comment_info['comment_time'] = current_time
        comment_info['user_id'] = user_id

        return session_info, comment_info

    def handle_comment_info_select(self, comment_info):
        '''

        :param comment_info:
        :return:
        :param comment_info_re
            :param username                     用户名
            :param comment_content              评论内容
            :param comment_time                 评论时间
        '''
        comment_info_list = []

        for item in comment_info:
            temp_dict = {}
            # 处理用户名
            username = item['username']
            username = username[0] + '***' + username[len(username) - 1]

            temp_dict['username'] = username
            temp_dict['profile_pic_url'] = item['profile_pic_url']
            temp_dict['comment_content'] = item['comment_content']
            temp_dict['comment_time'] = item['comment_time']

            comment_info_list.append(temp_dict)

        return comment_info_list

    def handle_category_info(self, category_info):
        '''
        处理商品分类信息
        :param category_info:
        :return:
        '''
        category_info_re = []

        for item in category_info:
            temp_dict = {}
            temp_dict['category_content'] = item['category_content']
            temp_dict['category_id'] = item['category_id']
            category_info_re.append(temp_dict)

        return category_info_re

    def handle_address_info(self, apply_info):

        '''
        处理地址信息
        :param apply_info:
        :return:
        '''
        session_info = apply_info['session_info']
        address_info = apply_info['address_info']

        user_id = int(session_info['session_id'][1:])

        address_info['user_id'] = user_id

        return session_info, address_info, user_id

    def handle_user_info(self, user_info):
        '''
        处理用户信息
        :param user_info:
        :return:
        '''
        user_info_re = {}

        username = user_info['username']
        telephone = user_info['telephone']

        user_info_re['username'] = username[0] + '***' + username[len(username)-1]
        user_info_re['telephone'] = telephone[0:2] + '****' + telephone[7:10]
        user_info_re['sex'] = user_info['sex']
        user_info_re['birthday'] = user_info['birthday']
        user_info_re['profile_pic_url'] = user_info['profile_pic_url']
        user_info_re['balance'] = user_info['balance']
        user_info_re['credits'] = user_info['credits']

        return user_info_re

    def handle_store_address(self, user_id):

        filename = setting.profile_pic_prifix + str(user_id) + setting.profile_pic_extension
        store_dict = setting.profile_pic_store_address + 'user/'

        store_address = store_dict + filename

        return store_address

    def handle_order_info(self, order_info):

        order_info_re = []

        for item in order_info:
            temp_dict = {}
            for key in item:
                if key != 'order_id' and key != 'user_id' and key!='user_id1' and key != 'confirm_time' \
                        and key != 'shipping_time' and key != 'next_pay_time'and key != 'alread_pay_month' \
                        and key != 'need_to_pay_month' and key != 'is_used'and key != 'e_ticket_id' \
                        and key != 'ticket_number' and key != 'order_id1'and key != 'create_time_eticket' \
                        and key != 'used_time':
                    temp_dict[key] = item[key]

                if item['product_type'] == 1:
                    need_to_pay = item['need_to_pay_month'] - item['already_pay_month']
                    shipping_str = '已付%d期还需付%d期<br>下次付款%s'%\
                                   (item['already_pay_month'], need_to_pay, item['next_pay_time'])
                    temp_dict['shipping_status'] = shipping_str
                elif item['product_type'] == 2:
                    if item['is_used'] == 0:
                        shipping_str = '未使用'
                    else:
                        shipping_str = '已使用'
                    temp_dict['shipping_status'] = shipping_str

            order_info_re.append(temp_dict)

        return order_info_re

    def handle_message_info(self, message_info):

        message_info_re = []

        for item in message_info:
            temp_dict = {}

            temp_dict['sender_name'] = '管理员'
            temp_dict['content'] = item['content']
            temp_dict['send_time'] = item['send_time']
            temp_dict['is_read'] = item['is_read']
            temp_dict['message_id'] = item['message_id']

            message_info_re.append(temp_dict)

        return message_info_re

    def handle_message_id_str(self, message_id_str):

        message_id_list = []
        m = message_id_str.split(',')
        for item in m:
            message_id_list.append(int(item))
        return message_id_list

    def handle_article_info(self, article_list_info, need_content):

        article_list_info_re = []
        for item in article_list_info:
            temp_dict = {}
            for key in item:
                if key != 'manager_id' and key != 'detail_img_url' and key != 'thumb_img_url'\
                        and key != 'is_delete' and key != 'hits_count' and key !='content':
                    temp_dict[key] = item[key]
            if need_content == 1:
                temp_dict['content'] = item['content']
                temp_dict['detail_img_url'] = item['detail_img_url']
            else:
                temp_dict['thumb_img_url'] = item['thumb_img_url']
            article_list_info_re.append(temp_dict)

        return article_list_info_re

    def handle_product_category_info(self, pro_category_info):

        pro_cate_info = ''
        for item in pro_category_info:
            pro_cate_info = pro_cate_info + item['category_content'] + ','
        if len(pro_cate_info) != 0:
            pro_cate_info = pro_cate_info[0:len(pro_cate_info)-1]
        return pro_cate_info
