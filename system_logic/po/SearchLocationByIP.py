# -*- coding: utf-8 -*-

import requests
import json
from system_logic.vo.method.DecodeJson import _decode_dict

class SearchLocationByIP:

    def search_location(self, client_ip):
        url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js&ip=' + client_ip
        re = requests.get(url=url)
        re_str = re.text
        try:
            ip_json = re_str.split(' = ')[1]
            ip_json = ip_json[0:len(ip_json) - 1]
            ip_info = _decode_dict(json.loads(str(ip_json)))
            if ip_info['ret'] == 1:
                country = ip_info['country']
                province = ip_info['province']
                city = ip_info['city']
            else:
                country = ''
                province = ''
                city = ''
        except:
            country = ''
            province = ''
            city = ''

        location_info = {
            'login_ip':client_ip,
            'country':country,
            'province':province,
            'city':city
        }

        return location_info
