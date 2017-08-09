# -*- coding: utf-8 -*-

#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine

class Message:

    def __init__(self):
        self.table_name = 'hf_message'

    def get_message(self, condition, supstring):
        tableName = [{'hf_message-hf_message_type':'message_type_id'}]
        de = DataBaseEngine(tableName)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        return result

    def insert_message(self, msg_info):
        de = DataBaseEngine(self.table_name)
        operate_type = 'insert'
        result = de.operate_database(operate_type=operate_type, operate_item=msg_info)
        return result

    def delete_message(self, condition):
        de = DataBaseEngine(self.table_name)
        operate_type = 'delete'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        return result

    def update_message(self, up_item, condition):
        de = DataBaseEngine(self.table_name)
        operate_type = 'update'
        result = de.operate_database(operate_type=operate_type, operate_item=up_item,operate_condition=condition)
        return result
