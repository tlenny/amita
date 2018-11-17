'''
Created on 2018年7月26日

@author: ALEX
'''
from analysis.voter import Voter
from data.model import BIAS, TradingDataDaily
import data.db_helper as db_helper
import analysis.trend as trend
import analysis.intersection as ins
import numpy as np


def query_kpi_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(BIAS.time_date, BIAS.bias_6, BIAS.bias_12, BIAS.bias_24, BIAS.bias_72).filter(BIAS.code == code, BIAS.time_date <= day).order_by(BIAS.time_date.desc()).limit(max_result)


def query_k_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= day).order_by(TradingDataDaily.time_date.desc()).limit(max_result)


class BIASVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
        
    def name(self):
        return 'BIAS'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(query_kpi_fn, (code, day, 30))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        b6_lines = values[:, 1].astype(float)
        b12_lines = values[:, 1].astype(float)
        b24_lines = values[:, 1].astype(float)
        
        if b6_lines[-1] <= -4 and b12_lines[-1] <= -5.5 and b24_lines[-1] <= -8:
            features.append(self.OVER_SOLD)
        
        if ins.match(b6_lines[-3:], b12_lines[-3:]) == 1 and ins.match(b6_lines[-3:], b24_lines[-3:]):
            features.append(self.GOOD_CROSS)
        
        if trend.is_uptrend(b6_lines[-10:]):
            k_values = db_helper.select(query_k_fn, (code, day, 10))
            k_values = np.array(k_values)[::-1]
            close_values = k_values[:, 0].astype(float)
            if trend.is_downtrend(close_values):
                features.append(self.BOTTOM_DEVIATION)
        return features
