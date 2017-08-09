# -*- coding: utf-8 -*-

import torndb

from system_logic import setting
from system_logic.dao.method.basicmethods.SqlMaking import selectConnectSheet_query


class SelectConnectSql:

    def __init__(self, table_dic, condition, supstring):
        '''

        :param table_dic:           所有连表的集合
        :param condition:           筛选条件

        数据结构
        table_dict = {'table1-table2':'colunmn_name'}       表示table1和table2连表查询，在colunmn_name列相等
        '''
        self.table_dic = table_dic
        self.condition = condition
        self.supstring = supstring
        self.select_item = {'*': 0}
        self.db = torndb.Connection(host=setting.host, database=setting.db, user=setting.user, password=setting.passwd)

    def select_connectSql(self):
        sql = selectConnectSheet_query(self.select_item, self.table_dic, self.condition, self.supstring)
        try:
            result = self.db.query(sql)
        except Exception as e:
            print e
            print sql
            return -1
        return result