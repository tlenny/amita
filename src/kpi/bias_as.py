# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月18日

@author: ALEX
'''

from data.model import BIAS, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

BIAS_N1, BIAS_N2, BIAS_N3, BIAS_N4 = 6, 12, 24, 72


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(BIAS_N4) 


def _bias_n(data, n):
    d = np.array(data[-n:])
    c = d[-1]
    ma = np.average(d)
    return np.float((c - ma) / ma * 100)


def _bias(code, data):
    bias = BIAS()
    bias.code = code
    bias.time_date = data[-1][0]
    close = np.array(data[:, 1].astype(float))
    bias.bias_6 = _bias_n(close, BIAS_N1)
    bias.bias_12 = _bias_n(close, BIAS_N2)
    bias.bias_24 = _bias_n(close, BIAS_N3)
    bias.bias_72 = _bias_n(close, BIAS_N4)
    return bias
    pass


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < BIAS_N4:
        return None
    data = np.array(data)
    rsi_list = []
    for i in range(len(data) - BIAS_N4 + 1):
        last_data = data[i:i + BIAS_N4]
        rsi = _bias(code, last_data)
        rsi_list.append(rsi)
    return rsi_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < BIAS_N4:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    rsi = _bias(code, data)
    return rsi


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
    calc('600004', None)
    pass
