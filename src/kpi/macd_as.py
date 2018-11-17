# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月12日

@author: ALEX
'''
from data.model import MACD, TradingDataDaily
import data.db_helper as db_helper
import numpy as np


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date == time_day).order_by(TradingDataDaily.time_date.desc()).limit(1) 


def query_macd_fn(sess, args):
    code = args[0]
    time_day = args[1]
    return sess.query(MACD.ema_12, MACD.ema_26, MACD.dea).filter(MACD.code == code, MACD.time_date < time_day).order_by(MACD.time_date.desc()).limit(1)


def _calc_macd(last_ema12, last_ema26, last_dea, close):
    ema12, ema26, dea = None, None, None
    if last_ema12 == None:
        ema12 = close
    else:
        ema12 = (last_ema12 * 11 + close * 2) / 13
    if last_ema26 == None:
        ema26 = close
    else:
        ema26 = (last_ema26 * 25 + close * 2) / 27
    dif = ema12 - ema26
    if last_dea == None:
        dea = dif
    else:
        dea = (last_dea * 8 + dif * 2) / 10
    
    ema12 = np.float(round(ema12, 4))
    ema26 = np.float(round(ema26, 4))
    dea = np.float(round(dea, 4))
    
    return ema12, ema26, dif, dea


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    data = np.array(data)
    macd_list = []
    last_ema12, last_ema26, last_dea = None, None, None
    for i in range(len(data)):
        close = np.float(data[i][1])
        ema12, ema26, dif, dea = _calc_macd(last_ema12, last_ema26, last_dea, close)
        last_ema12, last_ema26, last_dea = ema12, ema26, dea
        
        macd = MACD()
        macd.code = code
        macd.time_date = data[i][0]
        macd.ema_12 = ema12
        macd.ema_26 = ema26
        macd.dif = dif
        macd.dea = dea
        macd_list.append(macd)
    return macd_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) == 0:
        return
    data = np.array(data)
    close = np.float(data[0][1])
    
    last_ema12, last_ema26, last_dea = None,None,None
    last_macd = db_helper.select(query_macd_fn, (code, day))
    if len(last_macd) == 1:
        last_ema12 = np.float(last_macd[0][0])
        last_ema26 = np.float(last_macd[0][1])
        last_dea = np.float(last_macd[0][2])
    ema12, ema26, dif, dea = _calc_macd(last_ema12, last_ema26, last_dea, close)
    macd = MACD()
    macd.code = code
    macd.time_date = data[0][0]
    macd.ema_12 = ema12
    macd.ema_26 = ema26
    macd.dif = dif
    macd.dea = dea
    return macd


def calc(code, time_day):
    """
    time_date is None时初始化全量
            查询第一天的收盘价作为第一天的EMA12和EMA26
            第二天的ema = 前一日EMA×11/13+今日收盘价×2/13
    DIF=EMA12-EMA26
           今日DEA（MACD）=前一日DEA×8/10+今日DIF×2/10，其首日DEA为0
    BAR=2* (DIF-DEA)
    """
    if time_day == None:
        data = _init_all(code)
        if data != None and len(data) > 0:
            db_helper.batch_insert(data)
        return None
    else:
        return _init_day(code, time_day)


if __name__ == '__main__':
    pass
