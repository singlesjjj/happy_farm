# -*- coding: utf-8 -*-

import json
import urllib2
import memcache
import time
from system_logic import setting
#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine
#引入对象——人
from system_logic.bo.object.People import People
#引入对象——购物车
from system_logic.bo.object.static_object.Cart import Cart
#引入对象——消息
from system_logic.bo.object.static_object.Message import Message
#引入对象——新事件
from system_logic.bo.object.static_object.NewEvent import NewEvent
#引入数据处理模块
from system_logic.po.UserPO import UserPO
#引入session验证模块
from system_logic.po.VerifySession import VerifySession
#引入储存图片模块
from system_logic.po.UploadImg import UploadImg
#引入加密模块
from system_logic.po.EncryptString import EncryptString

class User:

    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'])
        self.up = UserPO()

    def login(self, apply_info):
        '''
        此方法用以实现允许用户登录
            1.将用户信息和数据库中信息进行比对,注意密码要经过md5加密后再比对
            2.若正确，将此次回话存入缓存，存入登录日志，并返回登录成功和session_id
            3.若错误，则返回登录失败
        :param apply_info:                   用户信息
            :param username                 用户名
            :param passwd                   密码
            :param login_ip                 登录ip
        数据结构
        user_info = {'username', 'password', 'login_ip'}

        :return: result
            -1                               连接失败
            0                                验证失败
            else                             成功
        '''
        p = People('user')
        result = p.login(apply_info)
        return result

    def register(self, apply_info):
        '''
        此方法用以实现用户注册，密码要经过md5加密再储存
        :param apply_info:
            :param username                 用户名
            :param passwd                   密码
            :param verify_code              手机验证码
            :param telephone                电话
            :param login_ip                 注册时ip
        数据结构
        user_info = {'username', 'password', 'telephone'}

        :return: result
            -1                               连接失败
            0                                用户名已存在
            -2                               电话已绑定
            -3                               手机验证吗验证失败
            else                             成功，返回session_id
        '''
        c1, c2, login_info, reg_info, verify_code = self.up.handle_registerInfo(apply_info)

        #判断手机验证码是否正确
        verify_code_mc = self.mc.get(reg_info['telephone'])
        if str(verify_code) != verify_code_mc['verify_code']:
            return -3
        self.mc.delete(reg_info['telephone'])
        #判断用户名和电话是否已存在
        r1 = self.get_user(c1)
        if r1:
            return 0
        r2 = self.get_user(c2)
        if r2:
            return -2

        #将用户注册信息写入用户表
        de = DataBaseEngine('hf_user')
        operate_type = 'insert'
        result = de.operate_database(operate_type=operate_type,operate_item=reg_info)
        if result == -1:
            return result

        #将用户注册事件写入事件表
        operate_item = {'event_type':1, 'event_name':'新用户注册', 'event_time':reg_info['register_time']}
        NewEvent().insert_event(operate_item)

        #登录用户，返回session_id
        result_login = self.login(login_info)
        return result_login

    def get_messageVerifyCode(self, telephone, template_id=setting.template_id):
        '''
        此方法用以让用户获取手机验证码
        :param telephone:                   手机号
        :return:
            -1                               连接失败
            1                                发送成功
        '''
        #获取请求参数
        url, account_sid, timestamp, responseMode, mc_value, body = self.up.handle_yunzhixunParas(telephone, template_id)

        #生成授权信息
        auth = self.up.handle_authInfo(account_sid, timestamp)

        #生成https请求报文
        req = urllib2.Request(url)
        req = self.up.createHttpReq(req, auth, responseMode, body)

        #发起请求
        try:
            res = urllib2.urlopen(req, data=None)
            data = res.read()
            res.close()
        except urllib2.HTTPError, error:
            data = error.read()
            error.close()

        #如果请求成功，将数据写入缓存，键为手机号
        data = json.loads(data)
        respCode = data['resp']['respCode']
        if respCode != '000000':
            return -1
        self.mc.set(telephone, mc_value, int(setting.code_expire)*60)
        return 1

    def browse_order(self, session_info, condition, page_number):

        '''
        此方法用以查看个人订单
        :param session_info
        :return:
        '''
        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        select_start = (page_number-1)*10
        table_name = [{'hf_order-hf_eticket':'order_id'}]
        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        supstring = ' ORDER BY create_time DESC LIMIT %d, 10'%(select_start)
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        if result == -1:
            return result,-1

        order_info = self.up.handle_order_info(result)

        if page_number == 1:
            de = DataBaseEngine('hf_order')
            select_item = {'COUNT(*)':0}
            operate_type = 'select'
            result = de.operate_database(operate_type=operate_type, operate_item=select_item, operate_condition=condition)
            count = result[0]['COUNT(*)']
        else:
            count = -1
        return order_info, count

    def browse_product(self, condition, page_number, each_page_products=12, supstring=None):
        result = People().browse_product(condition, page_number, each_page_products, supstring)
        if result == -1:
            return result
        product_info = self.up.handle_browse_product_info(result)
        return product_info

    def browse_product_by_category(self, condition, page_number, each_page_products=12, supstring=None):
        result = People().browse_product_by_category(condition, page_number, each_page_products, supstring)
        if result == -1:
            return result
        product_info = self.up.handle_browse_product_info(result)
        return product_info

    def add_product_to_cart(self, apply_info):
        '''
        此方法用以允许用户将商品添加至
        :param apply_info:                          请求信息
            :param session_info                     session信息
            :param product_info                     商品信息
                :param product_id                   商品id
                :param product_quantity             商品数量
        :return:
        -1                                           连接失败
        -2                                           session失效
        1                                            成功
        '''
        session_info, condition, cart_info = self.up.handle_cart_info(apply_info)

        #验证session的有效性
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        #查询购物车中是否已经有对应数据
        de = DataBaseEngine('hf_cart')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        if result == -1:
            return -1
        elif len(result) == 0:
            #将购物车信息写入数据库
            operate_type = 'insert'
            de.operate_database(operate_type=operate_type, operate_item=cart_info)
        else:
            #将购物车信息更新入数据库
            product_quantity_new = int(result[0]['product_quantity']) + int(cart_info['product_quantity'])
            add_time = cart_info['add_time']
            condition_new = {'cart_id=':result[0]['cart_id']}
            up_item = {'product_quantity':product_quantity_new,'add_time':add_time}
            Cart().update_cart(up_item,condition_new)
        return 1

    def change_cart(self, apply_info):
        '''

        :param apply_info:                  同上
        :return:
        '''
        session_info = apply_info['session_info']
        user_id = int(session_info['session_id'][1:])
        product_info = apply_info['product_info']
        product_id = product_info['product_id']
        condition = {'product_id=':product_id, 'user_id=':user_id}

        #验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        #更新购物车
        result = Cart().update_cart(product_info, condition)

        return result

    def browse_cart(self, session_info):
        '''

        :param session_info:                    同上
        :return:
        '''
        #验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        user_id = int(session_info['session_id'][1:])

        #获取对应购物车数据
        condition = {'user_id=':user_id, 'is_delete=':0}

        de = DataBaseEngine('hf_cart')
        operate_type = 'select'
        cart_info = de.operate_database(operate_type=operate_type, operate_condition=condition)

        if cart_info == -1:
            return cart_info

        #获取对应商品信息数据
        product_info_list = []
        for item in cart_info:
            condition_p = {'hf_product.product_id=':item['product_id']}
            product_info = self.browse_product(condition_p, 1)
            if product_info==-1 or len(product_info)==0:
                return -1
            product_info[0]['product_quantity'] = item['product_quantity']
            product_info_list.append(product_info[0])

        return product_info_list

    def write_comment(self, apply_info):
        '''
        此方法用于允许用户写评论
        :param apply_info:
            :param session_info
            :param comment_info
                :param product_id
                :param comment_content
        :return:
        '''
        session_info, comment_info = self.up.handle_comment_info(apply_info)

        #验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        #将评论写入数据库
        de = DataBaseEngine('hf_comment')
        operate_type = 'insert'
        result = de.operate_database(operate_type=operate_type, operate_item=comment_info)

        return result

    def get_comment(self, condition, page_number):
        '''

        :param condition:
        :return:
        '''
        result, count_num = People().get_comments(condition, page_number)

        if result == -1:
            return result

        comment_info = self.up.handle_comment_info_select(result)

        return comment_info, count_num

    def get_category(self, condition, supstring):

        category_info = People().get_category(condition, supstring)

        if category_info == -1:
            return category_info

        category_info = self.up.handle_category_info(category_info)

        return category_info

    def get_address(self, session_info):
        '''
        用户获取地址
        :param session_info:                    同上
        :return:
        '''

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        user_id = int(session_info['session_id'][1:])
        condition = {'user_id=':user_id}

        result = People().get_address(condition)

        return result

    def add_address(self, apply_info):
        '''
        添加地址
        :param apply_info:
            :param session_info
            :param address_info             地址信息
                :param country              国家
                :param province             省份
                :param city                 城市
                :param district             区县
                :param address_detail       地址详细
                :param zipcode              邮编
                :param contact_name         联系人名字
                :param contact_number       联系电话
                :param email                邮箱（可选）
        :return:
            -1                              连接错误
            -2                              session错误
            -3                              地址数量超出
            else
        '''

        session_info, address_info, user_id = self.up.handle_address_info(apply_info)

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        de = DataBaseEngine('hf_address')

        #查询当前用户有多少地址
        select_item = {'COUNT(*)':0}
        operate_type = 'select'
        condition = {'user_id = ':user_id}
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, operate_item=select_item)
        count = result[0]['COUNT(*)']

        if result == -1:
            return result
        #判断地址数量是否符合要求
        if count > 5:
            return -3

        #插入地址
        operate_type = 'insert'
        result = de.operate_database(operate_type=operate_type, operate_item=address_info)

        return result

    def delete_address(self, apply_info):

        '''
        删除地址
        :param apply_info:
            :param session_info
            :param address_info
                :param address_id
        :return:
        '''

        session_info = apply_info['session_info']
        address_info = apply_info['address_info']

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        user_id = int(session_info['session_id'][1:])
        address_id = address_info['address_id']
        condition = {'user_id = ':user_id, 'address_id = ':address_id}

        de = DataBaseEngine('hf_address')
        operate_type = 'delete'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        return result

    def get_user(self, session_info):
        '''
        获取用户信息
        :param session_info:
        :return:
        '''

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        user_id = session_info['session_id'][1:]
        condition = {'user_id=':user_id}

        result = People().get_user(condition)

        if result == -1:
            return result

        user_info = self.up.handle_user_info(result[0])

        return user_info

    def update_user(self, update_item, condition):
        '''

        :param update_item                  更新数据
        :param condition                    条件
        :return:
        '''
        de = DataBaseEngine('hf_user')
        operate_type = 'update'
        result = de.operate_database(operate_type=operate_type, operate_item=update_item, operate_condition=condition)
        return result

    def modify_user_info(self, apply_info):

        '''
        更新用户信息
        :param apply_info:
            :param session_info
            :param user_info
                :param sex
                :param birthday
        :return:
        '''
        session_info = apply_info['session_info']
        user_info = apply_info['user_info']
        user_id = int(session_info['session_id'][1:])
        condition = {'user_id=':user_id}
        update_item = {}

        if user_info.has_key('birthday'):
            update_item['birthday'] = user_info['birthday']

        if user_info.has_key('sex'):
            update_item['sex'] = user_info['sex']

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        result = self.update_user(update_item, condition)

        return result

    def upload_profile_pic(self, apply_info):
        '''
        上传用户头像
        :param apply_info:                      请求信息
            :param session_info
            :param pic_info
                :param base64_str               base64编码
        :return:
        '''
        session_info = apply_info['session_info']

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        user_id = int(session_info['session_id'][1:])
        base64_str = apply_info['pic_info']['base64_str']
        store_address = self.up.handle_store_address(user_id)

        store_url = UploadImg().create_img(base64_str, store_address)

        #将头像地址更新入用户表
        update_item = {'profile_pic_url':store_url}
        condition = {'user_id=':user_id}

        result = self.update_user(update_item, condition)

        return result

    def change_telephone(self, apply_info):

        '''
        允许用户修改电话号码
        :param apply_info:
            :param session_info             session信息
            :param tele_info                电话信息
                :param verify_code          验证码
                :param new_tele             新电话
        :return:
        -1                                   连接失败
        -2                                   session验证失败
        -3                                   验证码无效
        eles                                 成功
        '''
        session_info = apply_info['session_info']
        user_id = int(session_info['session_id'][1:])
        tele_info = apply_info['tele_info']
        user_info = People().get_user({'user_id=':user_id})
        if user_info == -1:
            return -1
        old_tele = user_info[0]['telephone']
        new_tele = tele_info['new_tele']
        verify_code = tele_info['verify_code']

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        #验证手机验证码
        verify_code_mc = self.mc.get(old_tele)
        if str(verify_code) != verify_code_mc['verify_code']:
            return -3
        self.mc.delete(old_tele)

        #将新手机更新入用户表
        update_item = {'telephone':new_tele}
        condition = {'user_id=':user_id}
        result = self.update_user(update_item,condition)
        return result

    def change_passwd(self, apply_info):
        '''
        允许用户修改密码
        :param apply_info:
            :param session_info
            :param passwd_info
                :param old_passwd
                :param new_passwd
        :return:
        -1                                      连接错误
        -2                                      session错误
        -3                                      旧密码错误
        else                                    成功
        '''
        session_info = apply_info['session_info']
        passwd_info = apply_info['passwd_info']
        old_passwd = EncryptString().encrypt_string(passwd_info['old_passwd'])
        new_passwd = EncryptString().encrypt_string(passwd_info['new_passwd'])
        user_id = int(session_info['session_id'][1:])

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        #判定旧密码是否正确
        de = DataBaseEngine('hf_user')
        condition = {'user_id':user_id, 'passwd':old_passwd}
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)

        if result == -1:
            return result
        elif result == []:
            return -3

        #将新密码写入
        update_item = {'passwd=':new_passwd}
        condition = {'user_id=':user_id}
        operate_type = 'update'
        result = de.operate_database(operate_type=operate_type, operate_item=update_item, operate_condition=condition)

        return result

    #未完成
    def refund_order(self, apply_info):

        '''
        允许用户退款
        :param apply_info:
            :param session_info
            :param refund_info
                :param order_id
                :param refund_reason
        :return:
        '''
        session_info = apply_info['session_info']

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

    def send_message_to_manager(self, apply_info):

        '''
        允许用户发送消息给管理员
        :param apply_info:
            :param session_info
            :param msg_info
                :param content
        :return:
        '''
        session_info = apply_info['session_info']
        msg_info = apply_info['msg_info']
        user_id = int(session_info['session_id'][1:])
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        msg_info['sender_id'] = user_id
        msg_info['receiver_id'] = 0
        msg_info['message_type_id'] = 1
        msg_info['send_time'] = current_time

        result = People().send_message(msg_info)

        # 将用户注册事件写入事件表
        operate_item = {'event_type': 2, 'event_name': '新消息', 'event_time': current_time}
        NewEvent().insert_event(operate_item)

        return result

    def browse_message(self, session_info, condition, page_number):

        '''
        允许用户查看自己的消息
        :param session_info:
        :return:
        '''
        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2,-1

        message_start = (int(page_number) - 1) * 15
        supstring = ' ORDER BY is_read ASC, send_time DESC LIMIT %d, 15'%(message_start)

        #获取对应消息数据
        de = DataBaseEngine('hf_message')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)

        if result == -1:
            return result,-1

        #获取总条数
        if page_number == 1:
            select_item = {'COUNT(*)': 0}
            count_num = de.operate_database(operate_type=operate_type, operate_item=select_item,
                                            operate_condition=condition)
            count_num = count_num[0]['COUNT(*)']
        else:
            count_num = -1

        #将is_alert字段更新为1
        for item in result:
            if item['is_alert'] == 0:
                condition = {'message_id=':item['message_id']}
                update_item = {'is_alert':1}
                Message().update_message(update_item, condition)

        message_info = self.up.handle_message_info(result)
        return message_info, count_num

    def get_new_message_count(self, session_info):

        '''
        获取新消息数量
        :param session_info:
        :return:
        '''
        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        user_id = int(session_info['session_id'][1:])
        condition = {'is_alert=':0, 'receiver_id=':user_id, 'message_type_id=':2, 'is_delete=':0}
        select_item = {'COUNT(*)':0}

        de = DataBaseEngine('hf_message')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_item=select_item, operate_condition=condition)

        if result == -1:
            return result
        return result[0]['COUNT(*)']

    def delete_message(self, session_info, message_id_str):

        '''
        删除消息
        :param session_info:
        :param message_id_str:                   信息id字符串1,2,3,4,...
        :return:
        '''
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        message_id_list = self.up.handle_message_id_str(message_id_str)
        result = People().delete_message(message_id_list)
        return result

    def mark_message_readed(self, session_info, message_id_str):

        # 验证session
        verify_result = VerifySession().verify_session_user(session_info)
        if not verify_result:
            return -2

        message_id_list = self.up.handle_message_id_str(message_id_str)
        result = People().mark_messageReaded(message_id_list)
        return result

    def browse_article_list(self, condition, page_number):

        '''
        允许用户选取文章信息
        :param condition:
        :param page_number:
        :return:
        '''
        article_start = (int(page_number)-1)*3

        supstring = 'ORDER BY is_top DESC, add_time DESC LIMIT %d, 3'%(article_start)
        result = People().browse_article(condition, supstring)

        if result == -1:
            return -1

        article_list_info = self.up.handle_article_info(result, 0)
        return article_list_info

    def browse_article_detail(self, condition):

        '''
        获取文章详细信息
        :param condition:
        :return:
        '''
        supstring = ''
        result = People().browse_article(condition, supstring)

        if result == -1:
            return -1

        article_detail_info = self.up.handle_article_info(result, 1)

        return article_detail_info

    def get_product_category(self,condition):

        table_name = [{'hf_product_category-hf_category':'category_id'}]
        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        if result == -1:
            return result
        category_info = self.up.handle_product_category_info(result)
        return category_info
