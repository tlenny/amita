# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月4日

@author: ALEX
'''

from data.model import MA, TradingDataDaily
import data.db_helper as db_helper
import numpy as np
import time
import analysis.linear_trend as linear_trend


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    limit = args[2]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(limit) 


def query_code_fn(sess, args):
    time_day = args[0]
    return sess.query(MA.code).filter(MA.time_date == time_day).distinct()


def query_ma_fn(sess, args):
    code = args[0]
    field = args[1]
    size = args[2]
    return sess.query(field).filter(MA.code == code, field != None).order_by(MA.time_date.desc()).limit(size)


def _calc(step, data):
    if len(data) < step:
        return None
    new_data = data[0 - step:, 1]
    new_data = np.average(new_data.astype(float))
    return np.float(round(new_data, 3))


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None, 250))
    data = np.array(data)
    data_size = len(data)
    if data_size < 5:
        return
    ma_list = []
    for i in range(data_size - 4):
        step = i + 4
        ma = MA()
        ma.code = code
        ma.time_date = data[step][0]
        ma.ma_5 = _calc(5, data[:step + 1])
        ma.ma_10 = _calc(10, data[:step + 1])
        ma.ma_20 = _calc(20, data[:step + 1])
        ma.ma_30 = _calc(30, data[:step + 1])
        ma.ma_60 = _calc(60, data[:step + 1])
        ma.ma_120 = _calc(120, data[:step + 1])
        ma.ma_250 = _calc(250, data[:step + 1])
        ma_list.append(ma)
    return ma_list


def _init_day(code, time_day):
    data = db_helper.select(query_data_fn, (code, time_day, 250))
    data = np.array(data)
    data_size = len(data)
    if data_size < 5:
        return None
    if data[0][0] == time_day:
        data = data[::-1]
        ma = MA()
        ma.code = code
        ma.time_date = data[-1][0]
        ma.ma_5 = _calc(5, data)
        ma.ma_10 = _calc(10, data)
        ma.ma_20 = _calc(20, data)
        ma.ma_30 = _calc(30, data)
        ma.ma_60 = _calc(60, data)
        ma.ma_120 = _calc(120, data)
        ma.ma_250 = _calc(250, data)
        return ma
    else :
        return None


def calc(code, time_day):
    if time_day == None:
        data = _init_all(code)
        if data != None and len(data) > 0:
            db_helper.batch_insert(data)
        return None
    else:
        return _init_day(code, time_day)
    

def _is_rebound(code, step=30, slide_days=10, turn_days=2):
    ma_values = db_helper.select(query_ma_fn, (code, MA.ma_30, 12))
    if len(ma_values) < 12:
        return False, ma_values
    ma_values = np.array(ma_values)
    ma_values = ma_values[:, 0]
    ma_values = ma_values.astype(float)
    pre_values = ma_values[0:slide_days]
    matched, a = linear_trend.match(pre_values, -1, 0, 0.2)
    if matched:
        low = ma_values[slide_days - 1]
        is_rebound = True
        for i in range(turn_days):
            if ma_values[slide_days + i] <= low:
                is_rebound = False
                break
        return is_rebound, ma_values
    else:
        return False, ma_values

        
def dig(step=30, slide_days=10, turn_days=2):
    day = time.strftime("%Y-%m-%d", time.localtime())
    code_list = db_helper.select(query_code_fn, (day,))
    rst = []
    for i in range(len(code_list)):
        code = code_list[i][0]
        is_rebound, ma_values = _is_rebound(code, step, slide_days, turn_days)
        print("分析[%s,%s]:%r" % ('ma', code, is_rebound))
        if is_rebound:
            data = db_helper.select(query_data_fn, (code, day, turn_days))
            data = np.array(data)
            data = data[:, 1]
            ma_values = ma_values[-turn_days:]
            is_less = np.min(np.less(ma_values, data))
            if is_less:
                rst.append(code)
    return rst


if __name__ == '__main__':
#     calc('600000',None)
#     is_rebound, ma_values = _is_rebound('300744', 30, 10, 1)
#     print(is_rebound)
#     _is_rebound('600000')
    data = dig()
    print(len(data))
    print(data)
