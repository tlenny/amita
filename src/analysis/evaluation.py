# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月17日

@author: ALEX
'''
from voter.ma_voter import MaVoter
from voter.arbr_voter import ArBrVoter
from voter.roc_voter import RocVoter
from voter.wr_voter import WRVoter
from voter.bias_voter import BIASVoter
from voter.vol_voter import VOLVoter
from voter.kdj_voter import KDJVoter
from voter.rsi_voter import RSIVoter
from voter.dmi_voter import DMIVoter
from voter.trix_voter import TRIXVoter
from voter.emv_voter import EMVVoter
from voter.dma_voter import DMAVoter
from voter.cr_voter import CRVoter
from voter.boll_voter import BOLLVoter
import data.db_helper as db_helper
from data.model import TradingDataDaily, Evaluation
from util.progress import Progress
import time
import numpy as np
import pandas as pd
import threading
import queue
from prettytable import PrettyTable

SAVE_DIR = 'D:/tomorrow/data/vote-result/'
VOTER_GROUP = [(MaVoter(), 1.0), (ArBrVoter(), 1.0), (RocVoter(), 1.0), (WRVoter(), 1.0), \
               (KDJVoter(), 1.0), (BIASVoter(), 1.0), (VOLVoter(), 2.0), (RSIVoter(), 1.0), \
               (DMIVoter(), 2.0), (TRIXVoter(), 1.0), (EMVVoter(), 1.0), (DMAVoter(), 1.0), \
               (CRVoter(), 1.0), (BOLLVoter(), 1.0)]
q = queue.Queue()
result = []
progress = Progress()


def query_code_fn(sess, args):
    time_day = args[0]
    return sess.query(TradingDataDaily.code).filter(TradingDataDaily.time_date == time_day).distinct()


def query_eval_fn(sess, args):
    day = args[0]
    max_result = args[1]
    return sess.query(Evaluation.code, Evaluation.score, Evaluation.feature).filter(Evaluation.time_date == day).order_by(Evaluation.score.desc()).limit(max_result)


def query_data_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    entity = args[3]
    return sess.query(entity).filter(entity.code == code, entity.time_date >= day).order_by(entity.time_date.asc()).limit(max_result)


def vote(day):
    while 1:
        if q.empty():
            break
        code = q.get()
        if code == None:
            break
        score, features = 0.0, []
        for j in range(len(VOTER_GROUP)):
            try:
                v = VOTER_GROUP[j][0]
                weight = VOTER_GROUP[j][1]
                tickets = v.vote(code, day)
                if tickets != None:
                    for i in range(len(tickets)):
                        score = score + tickets[i].weight * weight
                        features.append('%s-%s' % (v.name(), tickets[i].code))
            except Exception as e:
                print('评分失败:%s【%s】' % (code, v.name()))
        result.append([code, score, ','.join(features)])
        progress.log(progress.total - q.qsize())


def elect(day=None, max_result=20):
    if day == None:
        day = time.strftime("%Y-%m-%d", time.localtime())
    code_list = db_helper.select(query_code_fn, (day,))
    progress.setting(len(code_list), 5)
    for i in range(len(code_list)):
        code = code_list[i][0]
        q.put(code)
    thread_list = []
    for i in range(20):
        t = threading.Thread(target=vote, args=(day,))
        t.start()
        thread_list.append(t)
    
    for i in range(len(thread_list)):
        thread_list[i].join()
        
    sort_by = lambda elem:elem[1]
    rst = list(filter(lambda x:x[1] > 0, result))
    rst.sort(key=sort_by, reverse=True)
    print('')
    max_result = np.min([len(rst), np.int(max_result)])
    print('评估结果【正分%d，输出%d】：' % (len(rst), max_result))
    out = PrettyTable(['股票代码', '评分', '特征'])
    for i in range(max_result):
        out.add_row([rst[i][0], rst[i][1], rst[i][2]])
    print(out)
    
    entities = []
    for i in range(len(rst)):
        e = Evaluation()
        e.code = rst[i][0]
        e.time_date = day
        e.score = rst[i][1]
        e.feature = rst[i][2]
        entities.append(e)
    db_helper.batch_insert(entities)
        
    rst = np.array(rst)
    now = int(time.time()) 
    time_struct = time.localtime(now) 
    str_time = time.strftime("%Y%m%d%H%M", time_struct) 
    writer = pd.ExcelWriter(SAVE_DIR + 'R_%s.xlsx' % str_time)
    df = pd.DataFrame(data={'1:code':rst[:, 0], '2:score':rst[:, 1], '3:features':rst[:, 2]})
    df.to_excel(excel_writer=writer, sheet_name='buy', encoding="utf-8")
    writer.save()
    writer.close()


def _f(v, f='%.2f'):
    return f % v


def _f1(v):
    if v > 0:
        return '%.2f%%' % v
    else:
        return '--'

    
def eva(vote_day, count=10, days=5):
    query_data = db_helper.select(query_eval_fn, (vote_day, count))
    if len(query_data) == 0:
        elect(vote_day, count)
        query_data = db_helper.select(query_eval_fn, (vote_day, count))
    query_data = np.array(query_data)
    stock_codes = query_data[:, 0]
    scores = query_data[:, 1].astype(float)
    features = query_data[:, 2]
    
#     print(stock_codes)
    out = PrettyTable(['股票代码', '评分', '当日收盘价', '次日涨跌幅', '最高价' , '最低价', '最后收盘价', '最大涨幅' , '最大跌幅' , '后涨跌幅', '特征' ])
    for i in range(len(stock_codes)):
        values = db_helper.select(query_data_fn, (stock_codes[i], vote_day, days + 1, TradingDataDaily))
        values = np.array(values)
        close_values = np.array(list(map(lambda x:np.float(x.close), values)))
        high_values = np.array(list(map(lambda x:np.float(x.high), values)))
        low_values = np.array(list(map(lambda x:np.float(x.low), values)))
        close = np.float(close_values[0])
        delta_next, high, low, delta_high, last, delta_low, delta_close = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        if len(values) > 1:
            delta_next = np.float((np.float(close_values[1]) - close) / close * 100)
            last = np.float(close_values[-1])
            delta_close = np.float((last - close) / close * 100)
            high = np.float(np.max(high_values[1:]))
            low = np.float(np.max(low_values[1:]))
            delta_high = np.float((high - close) / close * 100)
            delta_low = np.max([np.float((close - low) / close * 100), 0])
        out.add_row([stock_codes[i], scores[i], _f(close), _f(delta_next, '%.2f%%'), _f(high), _f(low), _f(last), _f(delta_high, '%.2f%%'), _f1(delta_low), _f(delta_close, '%.2f%%'), features[i]])
    
    print('跟踪%s评估的%d只股票%d日内的价格情况' % (vote_day, count, days))
    print(out)
    pass 


def query_eval_his_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    lt = args[3]
    q = sess.query(Evaluation)
    if lt:
        q = q.filter(Evaluation.code == code, Evaluation.time_date <= day).order_by(Evaluation.score.desc())
    else:
        q = q.filter(Evaluation.code == code, Evaluation.time_date >= day).order_by(Evaluation.score.asc())
    return q.limit(max_result)


def query_data_his_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    entity = args[3]
    lt = args[4]
    q = sess.query(entity)
    if lt:
        q = q.filter(entity.code == code, entity.time_date <= day).order_by(entity.time_date.desc())
    else:
        q = q.filter(entity.code == code, entity.time_date >= day).order_by(entity.time_date.asc())
    return q.limit(max_result)


def his(code, day, day_len, forward):
    out = PrettyTable(['交易日', '收盘价', '涨跌幅', '评分', '特征' ])
    query_data = db_helper.select(query_data_his_fn, (code, day, day_len, TradingDataDaily, forward))
    query_data = np.array(query_data)
    close_values = np.array(list(map(lambda x:np.float(x.close), query_data)))
    open_values = np.array(list(map(lambda x:np.float(x.open), query_data)))
    days = np.array(list(map(lambda x:x.time_date, query_data)))
    
    query_data = db_helper.select(query_eval_his_fn, (code, day, day_len, forward))
    query_data = np.array(query_data)
    days2 = np.array(list(map(lambda x:x.time_date, query_data)))
    score_values = np.array(list(map(lambda x:np.float(x.score), query_data)))
    feature_values = np.array(list(map(lambda x:x.feature, query_data)))
    for i in range(len(days)):
        d = days[i]
        close = close_values[i]
        open_price = open_values[i]
        delta = np.float((close - open_price) / open_price * 100)
        index = -1
        for j in range(len(days2)):
            if days[i] == days2[j]:
                index = j
        score, feature = 0, ''
        if index >= 0:
            score = score_values[index]
            feature = feature_values[index]
        out.add_row([d, _f(close), _f(delta, '%.2f%%'), _f(score), feature])
    print(out)
    pass

        
if __name__ == '__main__':
#     print('%d%%%s' % (1, 5 * '*'))
#     elect()
#     ma = MaVoter()
#     ma.vote('000019', '2018-07-19')
    v = EMVVoter()
    v.vote('600004', '2018-07-27')
