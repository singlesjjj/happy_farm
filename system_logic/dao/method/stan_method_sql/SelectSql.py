# -*- coding: utf-8 -*-

import torndb

from system_logic import setting
from system_logic.dao.method.basicmethods.SqlMaking import select_query


class SelectSql:

    def __init__(self, table_name, select_item, condition, supstring, ):
        self.table_name = table_name
        self.condition = condition
        self.supstring = supstring
        if select_item != None:
            self.select_item = select_item
        else:
            self.select_item = {'*':0}
        self.db = torndb.Connection(host=setting.host, database=setting.db, user=setting.user, password=setting.passwd)

    def selelct_sql(self):
        sql = select_query(self.select_item, self.table_name, self.condition, self.supstring)
        try:
            result = self.db.query(sql)
        except Exception as e:
            print e
            print sql
            return -1
        return result