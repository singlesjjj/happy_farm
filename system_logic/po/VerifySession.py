# -*- coding: utf-8 -*-

import datetime
import memcache

class VerifySession:
    def __init__(self):
        self.nowtime = datetime.datetime.now()
        self.mc = memcache.Client(['127.0.0.1:11211'])

    def verify_session_manager(self, session_info):
        '''
        此方法用以验证session的有效性
        :param session_info:                        传入的session信息
            :param session_id                       session号
            :param verify_code                      验证码
        :param session_info_mem                     在高速缓存中的session信息
            :param expire                           session过期时间
            :param verify_code                      验证码
        :return:
            :param                                 True-验证通过，False-验证失败
        '''
        session_info_mem = self.mc.get(session_info['session_id'])
        if not session_info_mem:
            return False
        if session_info['verify_code'] == session_info_mem['verify_code']\
                and self.nowtime<session_info_mem['expire'] and session_info['session_id'][0] == 'm':
            return True
        return  False

    def verify_session_user(self, session_info):
        session_info_mem = self.mc.get(session_info['session_id'])
        if not session_info_mem:
            return False
        if session_info['verify_code'] == session_info_mem['verify_code'] \
                and self.nowtime < session_info_mem['expire'] and session_info['session_id'][0] == 'u':
            return True
        return False