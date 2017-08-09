# -*- coding: utf-8 -*-

import sys
import types

from system_logic import setting

reload(sys)
sys.setdefaultencoding('utf-8')

def select_query(item, sheet, condition, suppstring):
    select_str = selectStr(item)
    condition_str = conditionStr(condition)
    sheet = remake_sheetName(sheet)
    sql_select = 'SELECT '+select_str+' FROM '+sheet+' WHERE '+condition_str
    if suppstring:
        sql_select = sql_select + suppstring
    return sql_select

def selectConnectSheet_query(item, sheet_list, condition, suppstring):

    select_str = selectStr(item)
    condition_str = conditionStr(condition)
    sheet_str = connectSheet_str(sheet_list)
    sql_select = 'SELECT '+select_str+' FROM '+sheet_str+' WHERE '+condition_str
    if suppstring:
        sql_select = sql_select + suppstring
    return sql_select

def update_query(item, sheet, condition):
    update_str = updateStr(item)
    condition_str = conditionStr(condition)
    sheet = remake_sheetName(sheet)
    sql_update = 'UPDATE '+sheet+' SET '+update_str+\
                 ' WHERE '+condition_str
    return sql_update

def insert_query(item, sheet):
    select_str = selectStr(item)
    value_str = valueStr(item)
    sheet = remake_sheetName(sheet)
    sql_insert = 'INSERT INTO '+sheet+'('+select_str+') VALUES('+ value_str+')'
    return sql_insert

#insert into table_name(c1, c2, c3) values()
#[{'a':1,'b':2},{'a':3,'b':4}]
def insert_many_query(item, sheet):
    select_str = manySelectStr(item)
    manyValue_str = manyValueStr(item)
    sheet = remake_sheetName(sheet)
    sql_insert = 'INSERT INTO ' + sheet + '(' + select_str + ') VALUES(' + manyValue_str + ')'
    return sql_insert


def delete_query(sheet, condition):
    condition_str = conditionStr(condition)
    sheet = remake_sheetName(sheet)
    sql_delete = 'DELETE FROM '+sheet+' WHERE '+condition_str
    return sql_delete

def selectStr(item):
    select_str = ''
    for key in item:
        if key != 'type':
            select_str = select_str + str(key) + ','
    select_str = pop_str(select_str)
    return select_str

def manySelectStr(item_input):
    select_str = ''
    if len(item_input) == 0:
        return select_str
    for key in item_input[0]:
        select_str = select_str + str(key) + ','
    select_str = pop_str(select_str)
    return select_str

def updateStr(item):
    update_str = ''
    for key in item:
        if key!='type':
            if type(item[key]) is types.StringType:
                update_str = update_str + str(key) + '= "' + str(item[key]) + '",'
                #item[key] = unicode(item[key], "utf-8")
            else:
                update_str = update_str + str(key) + '= ' + str(item[key]) + ','
    update_str = pop_str(update_str)
    return update_str

def valueStr(item):
    value_str = ''
    for key in item:
        if key!='type':
            if type(item[key]) is types.StringType:
                value_str = value_str + '"' + str(item[key]) + '",'
            else:
                value_str = value_str + str(item[key]) + ','
    value_str = pop_str(value_str)
    return value_str

def manyValueStr(item):
    manyValue_str = ''
    for i in range(0, len(item[0])):
        manyValue_str = manyValue_str + '%s,'
    manyValue_str = pop_str(manyValue_str)
    return manyValue_str

def conditionStr(condition):
    #conditin = {'item<':123, 'bc>':2}
    #condition = [{'ab=':{'value':123, 'symbol':'OR'}}, {'cd=':{'value':321,'symbol':''}}]
    condition_str = ''
    if type(condition) is types.ListType:
        for item in condition:
            for key in item:
                value = item[key]['value']
                symbol = item[key]['symbol']
                condition_str = condition_str + get_condition_str(value, symbol, key)
    else:
        for key in condition:
            symbol = 'AND'
            value = condition[key]
            condition_str = condition_str + get_condition_str(value, symbol, key)
        if condition_str != '':
            for i in range(0,4):
                condition_str = pop_str(condition_str)
    return condition_str

def get_condition_str(value, symbol, key):

    condition_str = ''
    if type(value) is types.StringType and value != '':
        condition_str = condition_str + str(key) + '"' + str(value) + '" %s ' % (symbol)
    elif type(value) is types.StringType and value == '':
        condition_str = condition_str + str(key) + ' %s ' % (symbol)
    else:
        condition_str = condition_str + str(key) + str(value) + ' %s ' % (symbol)
    return condition_str

def pop_str(input_str):
    input_str = list(input_str)
    input_str.pop()
    input_str = ''.join(input_str)
    return input_str

def remake_sheetName(sheet):
    pre = setting.prefix
    #db_name = setting.db
    sheet = sheet.split(pre)
    sheet = sheet[len(sheet)-1]
    #sheet = db_name + '.' + pre + sheet
    sheet = pre + sheet
    return sheet

def connectSheet_str(sheet_list):
    sheet_str = ''
    used_table = []
    for item in sheet_list:
        table_names = item.keys()[0]
        table_list = table_names.split('-')
        for table in table_list:
            if len(used_table) == 0:
                sheet_str = sheet_str + table + ' '
                used_table.append(table)
            if table not in used_table:
                sheet_str = sheet_str + 'left join ' + table + ' '
                used_table.append(table)
        sheet_str = sheet_str + 'on ' + table_list[0] + '.' + item[table_names] + ' = ' + table_list[1] + '.'\
                    + item[table_names] + ' '
    return sheet_str

# input_1 =
# print insert_many_query(input_1, 'table_test')
