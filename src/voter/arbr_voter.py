'''
Created on 2018年7月19日

@author: ALEX
'''

from analysis.voter import Voter
from data.model import ARBR, TradingDataDaily
import data.db_helper as db_helper
import analysis.intersection as ins
import analysis.trend as trend
import numpy as np


def query_arbr_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(ARBR.time_date, ARBR.ar_26, ARBR.br_26).filter(ARBR.code == code, ARBR.time_date <= day).order_by(ARBR.time_date.desc()).limit(max_result)


def query_k_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= day).order_by(TradingDataDaily.time_date.desc()).limit(max_result)


class ArBrVoter(Voter):
    '''
    arbr指标趋势分析：
            金叉    0.5分   ：br从下向上突破ar
            底背离     1分    K线趋势下滑，arbr指标均上升，以14日做参考
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
        
    def name(self):
        return 'ARBR'
    
    def vote(self, code, day):
        features = []
        arbr_values = db_helper.select(query_arbr_fn, (code, day, 14))
        if len(arbr_values) < 14:
            return features
        arbr_values = np.array(arbr_values)[::-1]
        ar_values = arbr_values[:, 1].astype(float)
        br_values = arbr_values[:, 2].astype(float)
        if ins.match(br_values[-3:], ar_values[-3:]) == 1:
            features.append(self.GOOD_CROSS)
        
        if trend.is_uptrend(ar_values) and trend.is_uptrend(br_values):
            k_values = db_helper.select(query_k_fn, (code, day, 14))
            if len(k_values) == 14:
                k_values = np.array(k_values)[::-1]
                close_values = k_values[:, 0].astype(float)
                if trend.is_downtrend(close_values):
                    features.append(self.BOTTOM_DEVIATION)
            
        return features
