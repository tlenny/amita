'''
Created on 2018年8月1日

@author: ALEX
'''
from data.model import CR, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

CR_N = 26


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.open, TradingDataDaily.close, TradingDataDaily.high, TradingDataDaily.low).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.open, TradingDataDaily.close, TradingDataDaily.high, TradingDataDaily.low).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(CR_N + 1) 


def _cr_n(data):
    # CR（N日）=P1÷P2×100
    # P1=Σ（H－YM）
    # P2=Σ（YM－L）
    # M=（C+H+L+O）÷4
    p1, p2 = [], []
    for i in range(len(data) - 1):
        m = np.average(data[i, 1:5].astype(float))
        h = np.float(data[i + 1][3])
        l = np.float(data[i + 1][4])
        p1.append(h - m)
        p2.append(m - l)
    p1 = np.sum(p1)
    p2 = np.sum(p2)
    if p2 == 0:
        return 0
    else:
        return np.float(np.max([p1 / p2 * 100, 0]))


def _cr(code, data):
    entity = CR()
    entity.code = code
    entity.time_date = data[-1][0]
    entity.cr = _cr_n(data)
    return entity


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < CR_N + 1:
        return None
    data = np.array(data)
    entity_list = []
    for i in range(len(data) - CR_N):
        last_data = data[i:i + CR_N + 1]
        entity = _cr(code, last_data)
        entity_list.append(entity)
    return entity_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < CR_N + 1:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    entity = _cr(code, data)
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
