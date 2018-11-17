# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月3日

@author: ALEX
'''
from data.model import TradingDataDaily
import pandas as pd
import data.db_helper as db_helper
import os as os
import math

DATA_DIR = 'D:/tomorrow/data/'


def convert_num(v):
    if math.isnan(v):
        return None
    elif isinstance(v, int):
        return v
    elif isinstance(v, float):
        return v
    else:
        return None

    
def pack_data(d):
    data = TradingDataDaily()
    code = d[0]
    data.bourse = code[:2].upper()
    data.code = code[2:]
    data.time_date = d[1]
    data.open = convert_num(d[2])
    data.high = convert_num(d[3])
    data.low = convert_num(d[4])
    data.close = convert_num(d[5])
    data.change = convert_num(d[6])
    data.volume = convert_num(d[7])
    data.money = convert_num(d[8])
    data.traded_market_value = convert_num(d[9])
    data.market_value = convert_num(d[10])
    data.turnover = convert_num(d[11])
    data.adjust_price = convert_num(d[12])
    data.pe_ttm = convert_num(d[15])
    data.ps_ttm = convert_num(d[16])
    data.pc_ttm = convert_num(d[17])
    data.pb = convert_num(d[18])
    data.adjust_price_f = convert_num(d[19])
    return data
    

def init_data(file_name):
    f = open(file_name)
    df = pd.read_csv(f) 
    data = df.iloc[0:, :].values 
    data_list = []
    for i in range(len(data)):
        data_list.append(pack_data(data[i]))
    db_helper.batch_insert(data_list)
    print('导入数据%d条' % len(data_list))


def init_all():    
    list_file = os.listdir(DATA_DIR)
    for i in range(len(list_file)):
        print('初始化：%s\t\t%d/%d' % (list_file[i], (i + 1), len(list_file)))
        init_data(DATA_DIR + list_file[i])

    
if __name__ == '__main__':
    init_data(DATA_DIR + 'trading-data-push-20181105/2018-11-05 data.csv');
    pass
