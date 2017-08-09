# -*- coding: utf-8 -*-

import torndb

from system_logic import setting
from system_logic.dao.method.basicmethods.SqlMaking import delete_query


class DeleteSql:

    def __init__(self,table_name, condition):
        self.table_name = table_name
        self.condition = condition
        self.db = torndb.Connection(host=setting.host, database=setting.db, user=setting.user, password=setting.passwd)

    def delete_sql(self):
        sql = delete_query(self.table_name, self.condition)
        try:
            result = self.db.query(sql)
        except Exception as e:
            print e
            print sql
            return -1
        return result