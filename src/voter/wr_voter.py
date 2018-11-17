'''
Created on 2018年7月25日

@author: ALEX
'''

from analysis.voter import Voter
from data.model import WR, TradingDataDaily
import data.db_helper as db_helper
import analysis.trend as trend
import numpy as np


def query_wr_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(WR.time_date, WR.wr_6, WR.wr_10, WR.wr_20, WR.wr_40).filter(WR.code == code, WR.time_date <= day).order_by(WR.time_date.desc()).limit(max_result)


def query_k_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= day).order_by(TradingDataDaily.time_date.desc()).limit(max_result)


class WRVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''

    def name(self):
        return 'WR'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(query_wr_fn, (code, day, 30))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        wr_6_values = values[:, 1].astype(float)
        
        if trend.is_uptrend(wr_6_values[-10:]):
            k_values = db_helper.select(query_k_fn, (code, day, 10))
            if len(k_values) == 10:
                k_values = np.array(k_values)[::-1]
                close_values = k_values[:, 0].astype(float)
                if trend.is_downtrend(close_values):
                    features.append(self.BOTTOM_DEVIATION)
        
        if wr_6_values[-1] > 80:
            features.append(self.OVER_SOLD)
        return features
        
