# -*- coding: utf-8

from system_logic.dao.method.SqlMethod import SqlMethod

class DataBaseEngine:

    def __init__(self, table_name):
        self.sm = SqlMethod()
        self.table_name = table_name

    def operate_database(self, operate_type, operate_item = None, operate_condition = None, supstring = None):
        '''

        :param operate_type:                    操作类型(增,删,查,改)
                新增:insert
                查询:select
                删除:delete
                修改:update
        :param operate_item:                    操作数据
        :param operate_condition:               操作条件
        :return:
        '''
        operate_method_str = operate_type + '_sql'
        mtd = getattr(self.sm, operate_method_str)
        result = mtd(self.table_name, operate_item, operate_condition, supstring)
        return result
