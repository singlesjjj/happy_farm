# -*- coding: utf-8 -*-

#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine

class Article:

    def __init__(self):
        pass

    def get_article(self, condition, supstring):

        de = DataBaseEngine('hf_article')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        return result