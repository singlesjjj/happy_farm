# -*- coding: utf-8 -*-

#引入md5加密模块
import hashlib

class EncryptString:

    def __init__(self):
        pass

    def encrypt_string(self, input_string):
        '''
        此方法实现用md5加密输入字符串
        :param input_string:            输入字符串
        :return: encrypted_string       加密后字符串
        '''
        m1 = hashlib.md5()
        m1.update(input_string)
        encrypted_string = m1.hexdigest()
        return encrypted_string
