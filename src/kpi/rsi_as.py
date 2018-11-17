# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月18日

@author: ALEX
'''

from data.model import RSI, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

RSI_N1, RSI_N2, RSI_N3 = 6, 12, 24


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(RSI_N3 + 1) 


def _rsi_n(data, n):
    c = np.array(data[-n:]) - np.array(data[-(n + 1):-1])
    a = np.sum(list(filter(lambda x:x > 0, c)))
    b = np.sum(list(filter(lambda x:x < 0, c)))
    if a - b == 0:
        return 0
    else:
        return np.float(a / (a - b) * 100)


def _rsi(code, data):
    rsi = RSI()
    rsi.code = code
    rsi.time_date = data[-1][0]
    close = np.array(data[:, 1].astype(float))
    rsi.rsi_6 = _rsi_n(close, RSI_N1)
    rsi.rsi_12 = _rsi_n(close, RSI_N2)
    rsi.rsi_24 = _rsi_n(close, RSI_N3)
    return rsi
    pass


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < RSI_N3 + 1:
        return None
    data = np.array(data)
    rsi_list = []
    for i in range(len(data) - RSI_N3):
        last_data = data[i:i + (RSI_N3 + 1)]
        rsi = _rsi(code, last_data)
        rsi_list.append(rsi)
    return rsi_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < RSI_N3 + 1:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    rsi = _rsi(code, data)
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
    a = np.array([1, 1.2, 1.1, 1.5, 1.6, 1.7, 1.5])
    print(_rsi_n(a, 6))
    calc('600004', '2018-07-18')
    pass
