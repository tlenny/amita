# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月3日

@author: ALEX
'''

import data.db_helper as db_helper
from data.model import TradingDataDaily
from util.progress import Progress
import kpi.ma_as as ma
import kpi.macd_as as macd
import kpi.trix_as as trix
import kpi.kdj_as as kdj
import kpi.dmi_as as dmi
import kpi.arbr_as as arbr
import kpi.emv_as as emv
import kpi.boll_as as boll
import kpi.rsi_as as rsi
import kpi.bias_as as bias
import kpi.roc_as as roc
import kpi.wr_as as wr
import kpi.dma_as as dma
import kpi.cr_as as cr
import queue
import threading
import datetime
#'ma', 'macd', 'trix', 'kdj',
all_kpi_names = ['ma', 'macd', 'trix', 'kdj', 'dmi', 'arbr', 'emv', 'boll', 'rsi', 'bias','roc','wr','dma','cr']
# all_kpi_names = ['roc','wr','dma','cr']

q = queue.Queue()
THREAD_SIZE = 10;
progress = Progress()


def query_code_fn(sess, args):
    time_day = args[0]
    if time_day == None:
        return sess.query(TradingDataDaily.code).distinct()
    else:
        return sess.query(TradingDataDaily.code).filter(TradingDataDaily.time_date == time_day).distinct()


def init_kpi(kpi_name, time_day):
#     print('启动线程初始化【%s】' % kpi_name)
    data_list = []
    while 1:
        if q.empty():
            if len(data_list) > 0:
                db_helper.batch_insert(data_list)
#             print('线程结束，完成[%d]条' % len(data_list))
            break
        code = q.get()
        if code == None:
            if len(data_list) > 0:
                db_helper.batch_insert(data_list)
#             print('任务结束')
            break
        start_ts = datetime.datetime.now()
        data = None
        try:
            if kpi_name == 'ma':
                data = ma.calc(code, time_day)
            elif kpi_name == 'macd':
                data = macd.calc(code, time_day)
            elif kpi_name == 'trix':
                data = trix.calc(code, time_day)
            elif kpi_name == 'kdj':
                data = kdj.calc(code, time_day)
            elif kpi_name == 'dmi':
                data = dmi.calc(code, time_day)
            elif kpi_name == 'arbr':
                data = arbr.calc(code, time_day)
            elif kpi_name == 'emv':
                data = emv.calc(code, time_day)
            elif kpi_name == 'boll':
                data = boll.calc(code, time_day)
            elif kpi_name == 'rsi':
                data = rsi.calc(code, time_day)
            elif kpi_name == 'bias':
                data = bias.calc(code, time_day)
            elif kpi_name == 'roc':
                data = roc.calc(code, time_day)
            elif kpi_name == 'wr':
                data = wr.calc(code, time_day)
            elif kpi_name == 'dma':
                data = dma.calc(code, time_day)
            elif kpi_name == 'cr':
                data = cr.calc(code, time_day)
            end_ts = datetime.datetime.now()
            progress.log(progress.total - q.qsize())
            if time_day == None:
                print('完成初始化【%s】\t%s\t%ds\t剩余%d' % (kpi_name, code, (end_ts - start_ts).seconds, q.qsize()))
            if data != None:
                data_list.append(data)
        except Exception as e:
            print('计算失败【%s】\t%s\t%s' % (kpi_name, code, time_day))
            print(e)


def init_all(kpi_name): 
    code_list = db_helper.select(query_code_fn, (None,))
    start_ts = datetime.datetime.now()
    for i in range(len(code_list)):
        code = code_list[i][0]
        q.put(code)
    thread_list = []
    for i in range(THREAD_SIZE):
        t = threading.Thread(target=init_kpi, args=(kpi_name, None))
        t.start()
        thread_list.append(t)
    
    for i in range(len(thread_list)):
        thread_list[i].join()
        
    end_ts = datetime.datetime.now()
    print('完成初始化[%s]，总耗时：%ds' % (kpi_name, (end_ts - start_ts).seconds))


def init_day(time_day, kpi_name):
    code_list = db_helper.select(query_code_fn, (time_day,))
    start_ts = datetime.datetime.now()
    print('初始化%s' % kpi_name)
    progress.setting(len(code_list), 10)
    for i in range(len(code_list)):
        code = code_list[i][0]
        q.put(code)
    thread_list = []
    for i in range(THREAD_SIZE):
        t = threading.Thread(target=init_kpi, args=(kpi_name, time_day))
        t.start()
        thread_list.append(t)
    
    for i in range(len(thread_list)):
        thread_list[i].join()
        
    end_ts = datetime.datetime.now()
#     print('完成初始化[%s]，总耗时：%ds' % (kpi_name, (end_ts - start_ts).seconds))

    
if __name__ == '__main__':
#     init_all('ma');
    init_day('2018-07-10', 'ma')
    pass
