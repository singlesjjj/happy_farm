# -*- coding: utf-8 -*-

from system_logic.dao.method.stan_method_sql import SelectSql, DeleteSql, InsertSql, InsertManySql, SelectConnectSql, UpdateSql


class SqlMethod:

    def __init__(self):
        pass

    def select_sql(self, table_name, op_item, condition, supstring):
        ss = SelectSql.SelectSql(table_name, op_item,condition, supstring)
        result = ss.selelct_sql()
        return result

    def delete_sql(self, table_name, op_item, condition, supstring):
        ds = DeleteSql.DeleteSql(table_name, condition)
        result = ds.delete_sql()
        return result

    def insert_sql(self, table_name, op_item, condition, supstring):
        its = InsertSql.InsertSql(table_name, op_item)
        result = its.insert_sql()
        return result

    def insertMany_sql(self, table_name, op_item, condition, supstring):
        ims = InsertManySql.InsertManySql(table_name, op_item)
        result = ims.insertMany_sql()
        return result

    def selectconnect_sql(self, table_dic, op_item, condition, supstring):
        scs = SelectConnectSql.SelectConnectSql(table_dic, condition, supstring)
        result = scs.select_connectSql()
        return result

    def update_sql(self, table_name, op_item, condition, supstring):
        us = UpdateSql.UpdateSql(table_name, op_item, condition)
        result = us.update_sql()
        return result

