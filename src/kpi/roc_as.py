# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月24日

@author: ALEX

1、 AX=今天的收盘价—12天前的收盘价
2、 BX=12天前的收盘价
3、 ROC=AX/BX
'''

from data.model import ROC, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

ROC_N, ROC_M = 12, 6


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(ROC_N + ROC_M - 1) 


def _get_roc_value(data):
    ax = np.float(data[-1][1])
    bx = np.float(data[0][1])
    if bx == 0:
        return 0
    else:
        return np.float((ax - bx) / bx * 100)


def _roc(code, data):
    roc = ROC()
    roc.code = code
    roc.time_date = data[-1][0]
    v = []
    for i in range(ROC_M):
        v.append(_get_roc_value(data[-(ROC_N + i):len(data) - i]))
    roc.roc = v[0]
    roc.rocma = np.float(np.average(v))
    return roc


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < ROC_N + ROC_M - 1:
        return None
    data = np.array(data)
    roc_list = []
    for i in range(len(data) - (ROC_N + ROC_M - 1)):
        last_data = data[i:i + (ROC_N + ROC_M)]
        roc = _roc(code, last_data)
        roc_list.append(roc)
    return roc_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < ROC_N + ROC_M - 1:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    roc = _roc(code, data)
    return roc


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
