'''
Created on 2018年7月25日

@author: ALEX
'''
from analysis.voter import Voter
from data.model import KDJ, TradingDataDaily
import data.db_helper as db_helper
import analysis.trend as trend
import analysis.intersection as ins
import numpy as np


def query_kdj_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(KDJ.time_date, KDJ.k, KDJ.d, KDJ.j).filter(KDJ.code == code, KDJ.time_date <= day).order_by(KDJ.time_date.desc()).limit(max_result)


def query_k_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= day).order_by(TradingDataDaily.time_date.desc()).limit(max_result)


class KDJVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
        
    def name(self):
        return 'KDJ'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(query_kdj_fn, (code, day, 30))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        k_values = values[:, 1].astype(float)
        d_values = values[:, 2].astype(float)
        j_values = values[:, 3].astype(float)
        
        if k_values[-1] <= 20 and d_values[-1] <= 20 and j_values[-1] <= 20:
            features.append(self.OVER_SOLD)
        
        if ins.match(k_values[-3:], d_values[-3:]) == 1 and ins.match(j_values[-3:], d_values[-3:]):
            features.append(self.GOOD_CROSS)
        
        s = 0
        if trend.is_uptrend(k_values[-10:]):
            s = s + 1
        if trend.is_uptrend(d_values[-10:]):
            s = s + 1
        if trend.is_uptrend(j_values[-10:]):
            s = s + 1
        if s >= 2:
            k_values = db_helper.select(query_k_fn, (code, day, 10))
            k_values = np.array(k_values)[::-1]
            close_values = k_values[:, 0].astype(float)
            if trend.is_downtrend(close_values):
                features.append(self.BOTTOM_DEVIATION)
        return features
