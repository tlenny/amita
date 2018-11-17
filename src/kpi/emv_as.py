# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月17日

@author: ALEX
1.A=（今日最高+今日最低）/2
B=（前日最高+前日最低）/2
C=今日最高-今日最低
2.EM=（A-B）*C/今日成交额
3.EMV=N日内EM的累和
4.MAEMV=EMV的M日的简单移动平均
5.参数N为14，参数M为9
'''
from data.model import EMV, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

EMV_N, EMV_M, MU_FACTOR = 14, 9, 100000000


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.high, TradingDataDaily.low, TradingDataDaily.money).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.high, TradingDataDaily.low, TradingDataDaily.money).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(2) 


def query_emv_fn(sess, args):
    code = args[0]
    time_day = args[1]
    return sess.query(EMV.em, EMV.emv).filter(EMV.code == code, EMV.time_date < time_day).order_by(EMV.time_date.desc()).limit(EMV_N - 1)


def _emv(code, data, em_his, emv_his):
    emv = EMV()
    emv.time_date = data[-1][0]
    emv.code = code
    a = (np.float(data[-1][1]) + np.float(data[-1][2])) / 2
    b = (np.float(data[-2][1]) + np.float(data[-2][2])) / 2
    c = np.float(data[-1][1]) - np.float(data[-1][2])
    # EM=（A-B）*C/今日成交额
    _em = np.float((a - b) * c / np.float(data[-1][3]) * MU_FACTOR)
    
    em_his = np.append(em_his, np.array([_em]))
    if len(em_his) > EMV_N:
        em_his = np.delete(em_his, 0)
    _emv = np.float(np.sum(em_his))
    
    emv_his = np.append(emv_his, np.array([_emv]))
    if len(emv_his) > EMV_M:
        emv_his = np.delete(emv_his, 0)
    _maemv = np.float(round(np.average(emv_his), 6))
    
    emv.em = np.float(round(_em, 6))
    emv.emv = _emv
    emv.maemv = _maemv
    return emv, em_his, emv_his


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < 2:
        return None
    data = np.array(data)
    emv_list = []
    em_his, emv_his = np.array([]), np.array([])
    for i in range(len(data) - 1):
        last_data = data[i:i + 2]
        emv, em_his, emv_his = _emv(code, last_data, em_his, emv_his)
        emv_list.append(emv)
    return emv_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < 2:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    
    his = db_helper.select(query_emv_fn, (code, day))
    his = np.array(his)
    his = his[::-1]
    em_his = np.array(his[1 - EMV_N:, 0].astype(float))
    emv_his = np.array(his[1 - EMV_M:, 0].astype(float))
    emv, em_his, emv_his = _emv(code, data, em_his, emv_his)
    return emv


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
    calc('300015', '2018-07-18')
#     a = np.array([1,2,3,4])
#     a = np.delete(a, 0)
#     print(a)
    pass
