'''
Created on 2018年7月17日

@author: ALEX
'''
from data.model import TradingDataDaily
import data.db_helper as db_helper
import numpy as np


def query_single_fn(sess, args):
    code = args[0]
    start_day = args[1]
    end_day = args[2]
    query_field = args[3]
    return sess.query(query_field).filter(TradingDataDaily.code == code, TradingDataDaily.time_date >= start_day, TradingDataDaily.time_date <= end_day) 


class Feature(object):
    '''
    classdocs
    '''
    code, weight, desc = None, 1.0, None
    
    def __init__(self, code, weight, desc):
        '''
        Constructor
        '''
        self.code = code
        self.weight = weight
        self.desc = desc


class Voter(object):
    '''
            投票评分的基类，对每只股票进行投票评分，评分取值在-1到1之间，正数适合买入，负数适合卖出
    '''
    OVER_SOLD = Feature('CM', 0.5, '超卖')
    GOOD_CROSS = Feature('JC', 0.5, '金叉')
    BOTTOM_DEVIATION = Feature('DBL', 1, '底背离')
    REBOUND = Feature('FT', 1, '反弹')
    BREAK_ZERO = Feature('TP', 1, '突破零线')
    VOL_RISE = Feature('FL', 1, '放量')
    
    def vote(self, code, day):
        pass

    def weight(self):
        return 1.0
    
    def name(self):
        return "DEFAULT"

    def _get_close_price(self, code, start_day, end_day):
        data = db_helper.select(query_single_fn, (code, start_day, end_day, TradingDataDaily.close))
        if len(data) == 0:
            return None
        else:
            return np.array(data)[:, 0]
    
    def query_kpi_fn(self, sess, args):
        code = args[0]
        day = args[1]
        max_result = args[2]
        entity = args[3]
        return sess.query(entity).filter(entity.code == code, entity.time_date <= day).order_by(entity.time_date.desc()).limit(max_result)
    
    def __init__(self, params):
        '''
        Constructor
        '''
        
