# -*- coding: utf-8 -*-

class BrowseProductInputPO:

    def handle_browse_product_input(self, arguments):

        condition = {}
        page_number = 1
        each_page_products = 12
        supstring = None

        for key in arguments:
            if key == 'product_name':
                condition[key+' LIKE '] = '%%'+arguments[key][0]+'%%'
            elif key == 'page_number':
                page_number = arguments[key][0]
            elif key == 'each_page_products':
                each_page_products = arguments[key][0]
            elif key == 'product_id':
                condition['hf_product.'+key+'='] = int(arguments[key][0])
            elif key == 'product_type' or key == 'category_id':
                condition[key + '='] = int(arguments[key][0])
            else:
                pass

        if arguments.has_key('product_type'):
            product_type = int(arguments['product_type'][0])
            if product_type == 0:
                if arguments.has_key('left_price'):
                    condition['shop_price >'] = float(arguments['left_price'][0])
                if arguments.has_key('right_price'):
                    condition['shop_price <'] = float(arguments['right_price'][0])
                if arguments.has_key('sort_by'):
                    if arguments['sort_by'][0] == 'price_d':
                        supstring = ' shop_price DESC, '
                    elif arguments['sort_by'][0] == 'price_a':
                        supstring = ' shop_price ASC, '
                    elif arguments['sort_by'][0] == 'addtime':
                        supstring = ''
            else:
                if arguments.has_key('left_price'):
                    condition['first_pay >'] = float(arguments['left_price'][0])
                if arguments.has_key('right_price'):
                    condition['first_pay <'] = float(arguments['right_price'][0])
                if arguments.has_key('sort_by'):
                    if arguments['sort_by'][0] == 'price_d':
                        supstring = ' first_pay DESC, '
                    elif arguments['sort_by'][0] == 'price_a':
                        supstring = ' first_pay ASC, '
                    elif arguments['sort_by'][0] == 'addtime':
                        supstring = ''

        if condition.has_key('product_type=') and condition['product_type='] == 0:
            del condition['product_type=']
            condition['NOT product_type='] = 1

        return condition, page_number, each_page_products, supstring