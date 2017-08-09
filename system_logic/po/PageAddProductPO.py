# -*- coding: utf-8 -*-

class PageAddProductPO:

    def handle_category_list(self, category_list):

        '''

        :param category_list:
        :return:
        category_info = {'level_count', 'category_info':{'cate_1','cate_2'...}}
        '''
        category_info = {}

        #计算有多少级
        cate_sperate_list = []
        temp_list = category_list
        root_list = [0]
        count_used = 0
        while True:
            temp_sperate_list = []
            temp_root_list = []
            for item in temp_list:
                for parent_id in root_list:
                    if item['parent_category_id'] == parent_id:
                        temp_sperate_list.append(item)
                        temp_root_list.append(item['category_id'])
                        count_used = count_used+1
            cate_sperate_list.append(temp_sperate_list)
            root_list = temp_root_list
            if count_used == len(temp_list):
                break

        return cate_sperate_list

# test_list = [{'is_delete': 0L, 'category_id': 1L, 'category_content': u'\u52a8\u7269', 'parent_category_id': 0L},
#              {'is_delete': 0L, 'category_id': 2L, 'category_content': u'\u690d\u7269', 'parent_category_id': 0L},
#              {'is_delete': 0L, 'category_id': 3L, 'category_content': u'\u852c\u83dc', 'parent_category_id': 2L},
#              {'is_delete': 0L, 'category_id': 4L, 'category_content': u'\u6c34\u679c', 'parent_category_id': 2L},
#              {'is_delete': 0L, 'category_id': 5L, 'category_content': u'\u5bb6\u79bd', 'parent_category_id': 1L},
#              {'is_delete': 0L, 'category_id': 6L, 'category_content': u'\u5bb6\u755c', 'parent_category_id': 1L}]
# a= PageAddProductPO().handle_category_list(test_list)
# print a[0]
# print a[1]