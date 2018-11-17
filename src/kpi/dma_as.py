'''
Created on 2018年7月27日

@author: ALEX
DMA=股价短期平均值—股价长期平均值
AMA=DMA短期平均值
以求10日、50日为基准周期的DMA指标为例，其计算过程具体如下：
DMA（10）=10日股价平均值—50日股价平均值
AMA（10）=10日DMA平均值
'''

from data.model import DMA, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

DMA_N, DMA_M = 50, 10


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(DMA_N + DMA_N - 1) 


def _get_dma_value(data):
    v = data[:, 1].astype(float)
    ma_10 = np.average(v[-10:])
    ma_50 = np.average(v)
    return np.float(ma_10 - ma_50)


def _dma(code, data):
    dma = DMA()
    dma.code = code
    dma.time_date = data[-1][0]
    v = []
    for i in range(DMA_M):
        v.append(_get_dma_value(data[-(DMA_N + i):len(data) - i]))
    dma.dma = v[0]
    dma.ama = np.float(np.average(v))
    return dma


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < DMA_N + DMA_M - 1:
        return None
    data = np.array(data)
    roc_list = []
    for i in range(len(data) - (DMA_N + DMA_M - 1)):
        last_data = data[i:i + (DMA_N + DMA_M)]
        roc = _dma(code, last_data)
        roc_list.append(roc)
    return roc_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < DMA_N + DMA_M - 1:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    dma = _dma(code, data)
    return dma


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
