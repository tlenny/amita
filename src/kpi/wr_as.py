# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月25日

@author: ALEX

WR(N) = 100 * [ HIGH(N)-C ] / [ HIGH(N)-LOW(N) ]
'''

from data.model import WR, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

WR_6, WR_10, WR_20, WR_40 = 6, 10, 20, 40


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close, TradingDataDaily.high, TradingDataDaily.low).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close, TradingDataDaily.high, TradingDataDaily.low).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(WR_40) 


def _wr_n(data, n):
    # WR(N) = 100 * [ HIGH(N)-C ] / [ HIGH(N)-LOW(N) ]
    sub_data = data[-n:]
    c = np.float(sub_data[-1][1])
    h = np.max(sub_data[:, 2].astype(float))
    l = np.min(sub_data[:, 3].astype(float))
    if h == l:
        return 0
    else:
        return np.float((h - c) / (h - l) * 100)


def _wr(code, data):
    entity = WR()
    entity.code = code
    entity.time_date = data[-1][0]
    entity.wr_6 = _wr_n(data, WR_6)
    entity.wr_10 = _wr_n(data, WR_10)
    entity.wr_20 = _wr_n(data, WR_20)
    entity.wr_40 = _wr_n(data, WR_40)
    return entity


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < WR_40:
        return None
    data = np.array(data)
    entity_list = []
    for i in range(len(data) - WR_40 + 1):
        last_data = data[i:i + WR_40]
        entity = _wr(code, last_data)
        entity_list.append(entity)
    return entity_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < WR_40:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    entity = _wr(code, data)
    return entity


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
