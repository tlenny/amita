# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月12日

@author: ALEX
1．计算N天的收盘价的指数平均AX 
AX = (N日) 收盘价 * 2 /(N+1) + (N-1)日 AX (N-1) /(N+1) 
2．计算N天的AX的指数平均BX 
BX = (N日) AX * 2 /(N+1) + (N-1)日 BX (N-1) /(N+1) 
3．计算N天的BX的指数平均TRIX 
TRIX = (I日) BX * 2 /(N+1) + (N-1)日 TRIX (N-1) /(N+1) 
4．计算TRIX的m日移动平均TMA 
TMA = ((I-M)日TRIX累加) /M日
'''
from data.model import TRIX, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

TRIX_N, TRIX_M = 12, 20


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date == time_day).order_by(TradingDataDaily.time_date.desc()).limit(1) 


def query_trix_fn(sess, args):
    code = args[0]
    time_day = args[1]
    max_result = args[2]
    return sess.query(TRIX.ax, TRIX.bx, TRIX.trix, TRIX.tma).filter(TRIX.code == code, TRIX.time_date < time_day).order_by(TRIX.time_date.desc()).limit(max_result)


def _calc_trix(last_ax, last_bx, last_trix, close):
    ax, bx, trix = None, None, None
    if last_ax == None:
        ax, bx, trix = close, close, close
    else:
        ax = (last_ax * (TRIX_N - 1) + close * 2) / (TRIX_N + 1)
        bx = (last_bx * (TRIX_N - 1) + ax * 2) / (TRIX_N + 1)
        trix = (last_trix * (TRIX_N - 1) + bx * 2) / (TRIX_N + 1)
    
    ax = np.float(round(ax, 4))
    bx = np.float(round(bx, 4))
    trix = np.float(round(trix, 4))
    
    return ax, bx, trix


def _get_tma(last_tx_list, tx):
    last_tx_list = np.append(np.array(last_tx_list),np.array([tx]))
    last_tx_list = last_tx_list.astype(float)
    return np.float(round(np.average(last_tx_list), 4))


def _extact_tma(last_trix_list):
    last_tma_list = []
    for i in range(len(last_trix_list)):
        last_tma_list.append(np.float(last_trix_list[i].trix))
    return last_tma_list


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    data = np.array(data)
    trix_list = []
    last_ax, last_bx, last_trix = None, None, None
    for i in range(len(data)):
        close = np.float(data[i][1])
        ax, bx, tx = _calc_trix(last_ax, last_bx, last_trix, close)
        last_ax, last_bx, last_trix = ax, bx, tx
        
        trix = TRIX()
        trix.code = code
        trix.time_date = data[i][0]
        trix.ax = ax
        trix.bx = bx
        trix.trix = tx
        last_tma_list = trix_list[1 - TRIX_M:]
        trix.tma = _get_tma(_extact_tma(last_tma_list), tx)
        trix_list.append(trix)
    return trix_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) == 0:
        return
    data = np.array(data)
    close = np.float(data[0][1])
    
    last_ax, last_bx, last_trix = None, None, None
    last_data = db_helper.select(query_trix_fn, (code, day, 1))
    if len(last_data) == 1:
        last_ax = np.float(last_data[0][0])
        last_bx = np.float(last_data[0][1])
        last_trix = np.float(last_data[0][2])
    ax, bx, tx = _calc_trix(last_ax, last_bx, last_trix, close)
    trix = TRIX()
    trix.code = code
    trix.time_date = day
    trix.ax = ax
    trix.bx = bx
    trix.trix = tx
    last_tma_list = db_helper.select(query_trix_fn, (code, day, TRIX_M - 1))
    last_tma_list = np.array(last_tma_list)
    last_tma_list = last_tma_list[:, 2]
    trix.tma = _get_tma(last_tma_list, tx)
    return trix


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
    calc('600004','2018-07-13')
    pass
