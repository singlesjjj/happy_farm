# -*- coding: utf-8 -*-

#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine

class Product:

    def __init__(self):
        pass

    def insert_product(self, product_info):
        '''
        添加商品
        :return:
        :param product_id                   商品号
        '''
        de = DataBaseEngine('hf_product')
        operate_type = 'insert'
        result = de.operate_database(operate_type=operate_type, operate_item=product_info)
        return result

