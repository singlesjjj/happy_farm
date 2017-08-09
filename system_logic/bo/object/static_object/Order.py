# -*- coding: utf-8 -*-

#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine

class Order:

    def __init__(self):
        pass

    def get_order(self, condition, supstring=None):

        de = DataBaseEngine('hf_order')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        return result