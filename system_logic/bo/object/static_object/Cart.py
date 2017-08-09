# -*- coding: utf-8 -*-

#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine

class Cart:

    def __init__(self):
        pass

    def update_cart(self, up_item, condition):
        de = DataBaseEngine('hf_cart')
        operate_type = 'update'
        result = de.operate_database(operate_type=operate_type, operate_item=up_item, operate_condition=condition)
        return result