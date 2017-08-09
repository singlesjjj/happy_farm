# -*- coding: utf-8 -*-

import base64

class UploadImg:

    def create_img(self, base64_str, store_address):

        '''
        将base64字符串从新解码成为图片
        :param base65_str:                  base64字符串
        :param store_address                储存文件位置
        :return:
        :param img_url                      储存文件连接
        '''
        img_data = base64.b64decode(base64_str)
        target_img = open(store_address, 'wb')
        target_img.write(img_data)
        target_img.close()
        return store_address
