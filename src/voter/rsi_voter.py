'''
Created on 2018年7月26日

@author: ALEX
'''
from analysis.voter import Voter
from data.model import RSI, TradingDataDaily
import data.db_helper as db_helper
import analysis.trend as trend
import analysis.intersection as ins
import numpy as np


def query_kpi_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(RSI.time_date, RSI.rsi_6, RSI.rsi_12, RSI.rsi_24).filter(RSI.code == code, RSI.time_date <= day).order_by(RSI.time_date.desc()).limit(max_result)


def query_k_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= day).order_by(TradingDataDaily.time_date.desc()).limit(max_result)


class RSIVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''

    def name(self):
        return 'RSI'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(query_kpi_fn, (code, day, 30))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        rsi_6_lines = values[:, 1].astype(float)
        rsi_12_lines = values[:, 2].astype(float)
        rsi_24_lines = values[:, 3].astype(float)
        
        if rsi_6_lines[-1] <= 20:
            features.append(self.OVER_SOLD)
        
        if rsi_6_lines[-1] < 50 and rsi_12_lines[-1] < 50 and rsi_24_lines[-1] < 50:
            if ins.match(rsi_6_lines[-3:], rsi_12_lines[-3:]) == 1 and ins.match(rsi_6_lines[-3:], rsi_24_lines[-3:]):
                features.append(self.GOOD_CROSS)
        
        if trend.is_uptrend(rsi_6_lines[-10:]):
            k_values = db_helper.select(query_k_fn, (code, day, 10))
            if len(k_values) == 10:
                k_values = np.array(k_values)[::-1]
                close_values = k_values[:, 0].astype(float)
                if trend.is_downtrend(close_values):
                    features.append(self.BOTTOM_DEVIATION)
        
        return features
        
