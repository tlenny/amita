'''
Created on 2018年7月26日

@author: ALEX
'''

from analysis.voter import Voter
from data.model import TRIX, TradingDataDaily
import data.db_helper as db_helper
import analysis.trend as trend
import analysis.intersection as ins
import analysis.zero_line as zero_line
import numpy as np


def query_kpi_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(TRIX.time_date, TRIX.trix, TRIX.tma).filter(TRIX.code == code, TRIX.time_date <= day).order_by(TRIX.time_date.desc()).limit(max_result)


def query_k_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= day).order_by(TradingDataDaily.time_date.desc()).limit(max_result)


class TRIXVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
        
    def name(self):
        return 'TRIX'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(query_kpi_fn, (code, day, 30))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        trix_values = values[:, 1].astype(float)
        tma_values = values[:, 2].astype(float)
        if ins.match(trix_values[-3:], tma_values[-3:]) == 1:
            features.append(self.GOOD_CROSS)
        
        if trend.is_uptrend(trix_values):
            k_values = db_helper.select(query_k_fn, (code, day, 30))
            if len(k_values) == 30:
                k_values = np.array(k_values)[::-1]
                close_values = k_values[:, 0].astype(float)
                if trend.is_downtrend(close_values):
                    features.append(self.BOTTOM_DEVIATION)
        
        bt, l = zero_line.breakthrough(trix_values, 0)
        if bt and l <= 3:
            features.append(self.BREAK_ZERO)
        return features
        
