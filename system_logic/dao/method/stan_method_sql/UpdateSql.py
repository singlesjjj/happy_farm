# -*- coding: utf-8 -*-

import torndb

from system_logic import setting
from system_logic.dao.method.basicmethods.SqlMaking import update_query


class UpdateSql:

    def __init__(self, table_name, update_item, condition):
        self.table_name = table_name
        self.update_item = update_item
        self.condition = condition
        self.db = torndb.Connection(host=setting.host, database=setting.db, user=setting.user, password=setting.passwd)

    def update_sql(self):
        sql = update_query(self.update_item, self.table_name, self.condition)
        try:
            result = self.db.update(sql)
        except Exception as e:
            print e
            print sql
            return -1
        return result