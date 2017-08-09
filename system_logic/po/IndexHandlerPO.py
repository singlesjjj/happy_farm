# -*- coding: utf-8 -*-

import time

class IndexHandlerPO():

    def __init__(self):
        self.current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def handle_new_events_info(self, count_new_user, count_new_msg, count_new_order):

        new_events = []
        if count_new_user != 0:
            temp_dict = {'event_icon': 'icon-people', 'event_name': '新用户',
                         'event_des': '新添' + str(count_new_user) + '名用户', 'event_time': self.current_date,
                         'event_url': '#'}
            new_events.append(temp_dict)
        if count_new_msg != 0:
            temp_dict = {'event_icon': 'fa fa-envelope', 'event_name': '新消息',
                         'event_des': '新收' + str(count_new_msg) + '条消息', 'event_time': self.current_date,
                         'event_url': '#'}
            new_events.append(temp_dict)
        if count_new_order != 0:
            temp_dict = {'event_icon': 'fa fa-shopping-basket', 'event_name': '新订单',
                         'event_des': '新接' + str(count_new_order) + '份订单', 'event_time': self.current_date,
                         'event_url': '#'}
            new_events.append(temp_dict)

        return new_events