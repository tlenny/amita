# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月18日

@author: ALEX
（1）计算MA
MA=N日内的收盘价之和÷N
（2）计算标准差MD
MD=平方根（N-1）日的（C－MA）的两次方之和除以N
（3）计算MB、UP、DN线
MB=（N－1）日的MA
UP=MB+k×MD
DN=MB－k×MD
（K为参数，可根据股票的特性来做相应的调整，一般默认为2）
'''
from data.model import BOLL, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

BOLL_N = 20


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(BOLL_N + 1) 


def _boll(code, data):
    last_ma = np.average(data[:-1, 1].astype(float))
    _md = np.std(data[1:, 1].astype(float))
    _mid = last_ma
    _up = _mid + _md * 2
    _dn = _mid - _md * 2
    boll = BOLL()
    boll.code = code
    boll.time_date = data[-1][0]
    boll.md = np.float(_mid)
    boll.up = np.float(_up)
    boll.dn = np.float(_dn)
    return boll
    

def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < BOLL_N + 1:
        return None
    data = np.array(data)
    boll_list = []
    for i in range(len(data) - BOLL_N):
        last_data = data[i:i + (BOLL_N + 1)]
        boll = _boll(code, last_data)
        boll_list.append(boll)
    return boll_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < BOLL_N + 1:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    boll = _boll(code, data)
    return boll


def calc(code, time_day):
    """
    time_date is None时初始化全量
    """
    if time_day == None:
        data = _init_all(code)
        if data != None and len(data) > 0:
            pass
            db_helper.batch_insert(data)
        return None
    else:
        return _init_day(code, time_day)


if __name__ == '__main__':
    calc('300015', None)
    pass
