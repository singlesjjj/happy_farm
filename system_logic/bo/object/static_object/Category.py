# -*- coding: utf-8 -*-

#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine

class Category:

    def get_category(self, condition, supstring):
        '''
        依据条件获取商品分类
        :param condition:
        :return:
        '''
        de = DataBaseEngine('hf_category')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition, supstring=supstring)
        return result
