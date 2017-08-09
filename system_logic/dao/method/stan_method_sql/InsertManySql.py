# -*- coding: utf-8 -*-

import torndb

from system_logic import setting
from system_logic.dao.method.basicmethods.SqlMaking import insert_many_query

class InsertManySql:

    def __init__(self, table_name, insert_item):
        self.table_name = table_name
        self.insert_item = insert_item
        self.db = torndb.Connection(host=setting.host, database=setting.db, user=setting.user, password=setting.passwd)

    def insertMany_sql(self):
        sql = insert_many_query(self.insert_item, self.table_name)
        insert_tuple = []
        for item in self.insert_item:
            temp_tuple = []
            for key in item:
                temp_tuple.append(item[key])
            insert_tuple.append(tuple(temp_tuple))
        insert_tuple = tuple(insert_tuple)
        try:
            result = self.db.insertmany(sql, insert_tuple)
        except Exception as e:
            print e
            print sql
            return -1
        return result
