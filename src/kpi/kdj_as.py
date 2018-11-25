# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月12日

@author: ALEX

n日RSV=（Cn－Ln）/（Hn－Ln）×100
公式中，Cn为第n日收盘价；Ln为n日内的最低价；Hn为n日内的最高价。
其次，计算K值与D值：
当日K值=2/3×前一日K值+1/3×当日RSV
当日D值=2/3×前一日D值+1/3×当日K值
若无前一日K 值与D值，则可分别用50来代替。
J值=3*当日K值-2*当日D值
'''
from data.model import KDJ, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

KDJ_N = 9


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close, TradingDataDaily.high, TradingDataDaily.low).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close, TradingDataDaily.high, TradingDataDaily.low).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(KDJ_N) 


def query_kdj_fn(sess, args):
    code = args[0]
    time_day = args[1]
    return sess.query(KDJ.k, KDJ.d).filter(KDJ.code == code, KDJ.time_date < time_day).order_by(KDJ.time_date.desc()).limit(1)


def _rsv(last_data):
    # （Cn－Ln）/（Hn－Ln）×100
    c = np.float(last_data[-1, 1])
    h = np.float(np.max(last_data[:, 2].astype(float)))
    l = np.float(np.min(last_data[:, 3].astype(float)))
    if h == l:
        return 0
    else:
        return np.float(round((c - l) / (h - l) * 100, 4))


def _calc_kdj(code, last_data, last_k, last_d):
    last_data = np.array(last_data)
    kdj = KDJ()
    kdj.code = code
    kdj.time_date = last_data[-1][0]
    rsv = _rsv(last_data)
    k = np.float(round((rsv + last_k * 2) / 3, 4))
    d = np.float(round((k + last_d * 2) / 3, 4))
    j = 3 * k - 2 * d
    kdj.rsv = rsv
    kdj.k = k
    kdj.d = d
    kdj.j = j
    return kdj


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < KDJ_N:
        return None
    data = np.array(data)
    kdj_list = []
    last_k, last_d = 50, 50
    for i in range(len(data) - KDJ_N + 1):
        last_data = data[i:KDJ_N + i]
        kdj = _calc_kdj(code, last_data, last_k, last_d)
        last_k, last_d = kdj.k, kdj.d
        kdj_list.append(kdj)
    return kdj_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < KDJ_N:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    last_kdj = db_helper.select(query_kdj_fn, (code, day))
    last_k, last_d = 50, 50
    if len(last_kdj) == 1:
        last_kdj = np.array(last_kdj)
        last_k, last_d = np.float(last_kdj[0][0]), np.float(last_kdj[0][1])
    return _calc_kdj(code, data, last_k, last_d)


def calc(code, time_day):
    """
    time_date is None时初始化全量
    """
    if time_day == None:
        data = _init_all(code)
        if data != None and len(data) > 0:
            db_helper.batch_insert(data)
        return None
    else:
        return _init_day(code, time_day)


if __name__ == '__main__':
    import datetime
    start_ts = datetime.datetime.now()
    calc('600653', None)
    end_ts = datetime.datetime.now()
    print((end_ts - start_ts).seconds)
    pass
