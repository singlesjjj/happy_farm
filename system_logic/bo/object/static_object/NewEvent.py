# -*- coding: utf-8 -*-

#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine

class NewEvent:

    def __init__(self):
        pass

    def insert_event(self, insert_item):

        de = DataBaseEngine('hf_new_event')
        operate_type = 'insert'
        result = de.operate_database(operate_item=insert_item, operate_type=operate_type)
        return result