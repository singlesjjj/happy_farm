# -*- coding: utf-8 -*-

class GetIdFromSession:

    def __init__(self):
        pass

    def get_id_from_session(self, session_info):
        '''
        此方法用以从session中获取id和对应的表
        :param session_info:                        传入的session信息
            :param session_id                       session号
            :param verify_code                      验证码
        :return:
            :param applicant_id                     请求者id
            :param table_name                       对应表名
        '''
        session_id = session_info['session_id']
        applicant_type = session_id[0]
        applicant_id = int(session_id[1:])

        if applicant_type == 'u':
            table_name = 'user'
        else:
            table_name = 'manager'

        return applicant_id, table_name
