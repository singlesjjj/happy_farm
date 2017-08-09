# -*- coding: utf-8 -*-


class WebMessagePO:

    def handle_input_condition(self, box_type, condition, manager_id):
        #用户收件箱
        if box_type == 1:
            condition['message_type_id='] = 1
            condition['receiver_id='] = 0
            condition['is_delete='] = 0
            title_name = '用户收件箱'
        #内部收件箱
        elif box_type == 2:
            condition['message_type_id='] = 3
            condition['receiver_id='] = manager_id
            condition['is_delete='] = 0
            title_name = '内部收件箱'
        #发件箱
        elif box_type == 3:
            condition['sender_id='] = manager_id
            condition['is_delete='] = 0
            title_name = '发件箱'

        #重要邮件
        elif box_type == 4:
            condition['is_important='] = 1
            condition['receiver_id='] = manager_id
            condition['is_delete='] = 0
            title_name = '重要邮件'
        #垃圾箱
        elif box_type == 5:
            condition['is_delete='] = 1
            condition['receiver_id='] = manager_id
            title_name = '垃圾箱'
        else:
            title_name = ''

        return condition, title_name