# -*- coding: utf-8 -*-
from random import Random

class ProduceRandomStr:

    def produce_randomStr(self):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = 16
        random = Random()
        for i in range(length):
            str += chars[random.randint(0, length)]
        return str

    def product_randomInt(self):
        str = ''
        chars = '0123456789'
        length = 4
        random = Random()
        for i in range(length):
            str += chars[random.randint(0, length)]
        return str

