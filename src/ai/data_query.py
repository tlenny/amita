'''
Created on 2018年7月31日

@author: ALEX
'''
from data.model import *
import data.db_helper as db
import numpy as np

comm_fields = ['open', 'close', 'high', 'low', 'change', 'volume', 'money', 'traded_market_value', 'market_value', 'turnover', 'adjust_price', 'pe_ttm', 'ps_ttm', 'pc_ttm', 'pb']
# comm_fields = ['open', 'close', 'high', 'low', 'change', 'volume', 'money']

entitys = [MA, MACD, ARBR, BIAS, BOLL, DMA, DMI, EMV, KDJ, ROC, RSI, TRIX, WR, CR]
# entitys = []

PREDICTED_RANGE = 10


def _attr(e):
    attr = dir(e)
    attr = list(filter(lambda x:x[0] != '_' and x != 'metadata' and x != 'id' and x != 'code' and x != 'time_date' and x != 'bourse' and x != 'created_stamp' , attr))
    return attr


def get_select_fields_count():
    count = len(comm_fields)  # len(_attr(TradingDataDaily))
    for i in range(len(entitys)):
        e = entitys[i]
        count = count + len(_attr(e))
    return count


def build_sql(code, start_day, end_day):
    sql = 'SELECT m0.open'
#     attr = _attr(TradingDataDaily)
    for i in range(len(comm_fields)):
        if comm_fields[i] == 'open':
            continue
        sql = sql + ', m0.%s' % comm_fields[i]
#             
    for i in range(len(entitys)):
        e = entitys[i]
        attr = _attr(e)
        for j in range(len(attr)):
            sql = sql + ',m%d.%s' % (i + 1, attr[j])
    sql = sql + ' FROM trading_data_daily m0 ' 
    for i in range(len(entitys)):
        e = entitys[i]
        sql = sql + ' LEFT OUTER JOIN %s m%d ON m%d.`code`=m0.`code` AND m%d.time_date=m0.time_date' % (e.__tablename__, i + 1, i + 1, i + 1)
    sql = sql + ' WHERE m0.code=\'%s\' ' % code
    if start_day != None:
        sql = sql + 'AND m0.time_date>=\'%s\' ' % start_day
    if end_day != None:
        sql = sql + 'AND m0.time_date<=\'%s\' ' % end_day
    for i in range(len(entitys)):
        e = entitys[i]
        attr = _attr(e)
        for j in range(len(attr)):
            sql = sql + ' AND m%d.%s IS NOT NULL' % (i + 1, attr[j])
    sql = sql + ' order by m0.time_date asc'
    return sql


def trend(x):
    x1 = x[0]
    if x1 == 0:
        return [0]
    else:
#         return [np.float(round((xm - x1) / x1, 4))]
        #[0,10%]区间认为盘整 0，大于该区间任务 上涨 1，小于该区间认为下跌 -1
        xm = np.max(x[1:])
        delta = np.float(round((xm - x1) / x1,1))
        if delta >= 1:
            return [0.9]
        elif delta < -1:
            return [-1]
        else:
            return [delta]
#         if delta > 0.1 :
#             return [1]
#         elif delta < 0 :
#             return [-1]
#         else:
#             return [0]


def query_data(code, start_day=None, end_day=None):
    sql = build_sql(code, start_day, end_day)
    print(sql)
    query = db.selectSql(sql)
    query = np.array(query).astype(float)
    x_list, y_list = [], []
    for i in range(len(query) - PREDICTED_RANGE):
        x = query[i]
        c = query[i:i + PREDICTED_RANGE + 1, 1]
        x_list.append(x.tolist())
        y_list.append(trend(c))
    return x_list, y_list


if __name__ == '__main__':
    print(build_sql('600004', None, '2018-03-01'))
    x, y = query_data('600004', '2018-03-01', '2018-04-01')
    print(x)
    print(y)
