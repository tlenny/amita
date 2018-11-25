# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月17日

@author: ALEX

AR计算公式
AR=((H - O)26天之和/(O - L)26天之和) * 100
H：当天之最高价
L：当天之最低价
O：当天之开盘价
BR计算公式
BR=((H - PC)26天之和/(PC - L)26天之和) * 100
H：当天之最高价；
L：当天之最低价；
PC：昨天之收盘价；
'''

from data.model import ARBR, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

ARBR_N = 26


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.open, TradingDataDaily.high, TradingDataDaily.low, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.open, TradingDataDaily.high, TradingDataDaily.low, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(ARBR_N + 1) 


def _ar(data):
    # ((H - O)26天之和/(O - L)26天之和) * 100
    h_o, o_l = [], []
    for i in range(len(data) - 1):
        o = np.float(data[i + 1][1])
        h = np.float(data[i + 1][2])
        l = np.float(data[i + 1][3])
        h_o.append(h - o)
        o_l.append(o - l)
    sum_h_o = np.sum(h_o)
    sum_o_l = np.sum(o_l)
    if sum_o_l == 0:
        return 0
    else:
        return np.float(round(sum_h_o / sum_o_l * 100, 4))


def _br(data):
    # BR=((H - PC)26天之和/(PC - L)26天之和) * 100
    h_pc, pc_l = [], []
    for i in range(len(data) - 1):
        pc = np.float(data[i][4])
        h = np.float(data[i + 1][2])
        l = np.float(data[i + 1][3])
        h_pc.append(h - pc)
        pc_l.append(pc - l)
    sum_h_pc = np.sum(h_pc)
    sum_pc_l = np.sum(pc_l)
    if sum_pc_l == 0:
        return 0
    else:
        return np.float(round(sum_h_pc / sum_pc_l * 100, 4))


def _arbr(code, data):
    arbr = ARBR()
    arbr.time_date = data[-1][0]
    arbr.code = code
    arbr.ar_26 = _ar(data)
    arbr.br_26 = _br(data)
    return arbr


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < ARBR_N + 1:
        return None
    data = np.array(data)
    arbr_list = []
    for i in range(len(data) - ARBR_N - 1):
        last_data = data[i:i + ARBR_N + 1]
        arbr_list.append(_arbr(code, last_data))
    return arbr_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < ARBR_N + 1:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    return _arbr(code, data)


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
    a = [1, 2, 3, 4]
    print(np.sum(a))
#     _init_all('000001')
    pass
