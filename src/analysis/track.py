# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月31日

@author: ALEX
'''
from prettytable import PrettyTable
import data.db_helper as db_helper
import numpy as np
from data.model import TradingDataDaily, Evaluation

DATA_PATH = 'D:/tomorrow/data/vote-result/'


def query_data_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    entity = args[3]
    return sess.query(entity).filter(entity.code == code, entity.time_date >= day).order_by(entity.time_date.asc()).limit(max_result)


def query_eval_fn(sess, args):
    day = args[0]
    max_result = args[1]
    return sess.query(Evaluation.code, Evaluation.score, Evaluation.feature).filter(Evaluation.time_date == day).order_by(Evaluation.score.desc()).limit(max_result)


def _f(v, f='%.2f'):
    return f % v


def _f1(v):
    if v > 0:
        return '%.2f%%' % v
    else:
        return '--'


def trace(vote_day, count=10, days=5):
#     str = vote_day[0:4] + vote_day[5:7] + vote_day[8:10]
#     file_name = DATA_PATH + 'R_%s.txt' % str
#     stock_codes = []
#     with open(file_name, 'r') as file_to_read:
#         while True:
#             lines = file_to_read.readline()  # 整行读取数据
#             if not lines:
#                 break
#             stock_codes.append(lines.split()[0])
    query_data = db_helper.select(query_eval_fn, (vote_day, count))
    query_data = np.array(query_data)
    stock_codes = query_data[:, 0]
    scores = query_data[:, 1].astype(float)
    features = query_data[:, 2]
    
#     print(stock_codes)
    out = PrettyTable(['股票代码', '评分', '当日收盘价', '次日涨跌幅', '期内最高价' , '期内最低价', '期后收盘价', '期内最大涨幅' , '期内最大跌幅' , '期后涨跌幅', '特征' ])
    for i in range(len(stock_codes)):
        values = db_helper.select(query_data_fn, (stock_codes[i], vote_day, days + 1, TradingDataDaily))
        values = np.array(values)
        close_values = np.array(list(map(lambda x:np.float(x.close), values)))
        high_values = np.array(list(map(lambda x:np.float(x.high), values)))
        low_values = np.array(list(map(lambda x:np.float(x.low), values)))
        close = np.float(close_values[0])
        delta_next = np.float((np.float(close_values[1]) - close) / close * 100)
        high = np.float(np.max(high_values[2:]))
        low = np.float(np.max(low_values[2:]))
        delta_high = np.float((high - close) / close * 100)
        last = np.float(close_values[-1])
        delta_low = np.max([np.float((close - low) / close * 100), 0])
        delta_close = np.float((last - close) / close * 100)
        out.add_row([stock_codes[i], scores[i], _f(close), _f(delta_next, '%.2f%%'), _f(high), _f(low), _f(last), _f(delta_high, '%.2f%%'), _f1(delta_low), _f(delta_close, '%.2f%%'), features[i]])
    
    print('跟踪%s评估的%d只股票%d日内的价格情况' % (vote_day, count, days))
    print(out)
    pass


if __name__ == '__main__':
#     trace('2018-07-26', 10, 10)
    a = np.array([1.0, 2, None])
    if None in a:
        print('OK')
    else:
        print('NO')
    pass
