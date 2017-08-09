# -*- coding: utf-8 -*-

import torndb

from system_logic import setting
from system_logic.dao.method.basicmethods.SqlMaking import insert_query


class InsertSql:

    def __init__(self, table_name, insert_item):
        self.table_name = table_name
        self.insert_item = insert_item
        self.db = torndb.Connection(host=setting.host, database=setting.db, user=setting.user, password=setting.passwd)

    def insert_sql(self):
        sql = insert_query(self.insert_item, self.table_name)
        try:
            result = self.db.insert(sql)
        except Exception as e:
            print e
            print sql
            return -1
        return result