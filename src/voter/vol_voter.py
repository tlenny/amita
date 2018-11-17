'''
Created on 2018年7月26日

@author: ALEX
'''

from analysis.voter import Voter
from data.model import TradingDataDaily
import data.db_helper as db_helper
import numpy as np


def query_k_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(TradingDataDaily.volume).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= day).order_by(TradingDataDaily.time_date.desc()).limit(max_result)


class VOLVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
        
    def name(self):
        return 'VOL'
    
    def vote(self, code, day):
        features = []
        k_values = db_helper.select(query_k_fn, (code, day, 6))
        if len(k_values) < 6:
            return features
        k_values = np.array(k_values)[::-1]
        vol_values = k_values[:, 0].astype(float)
        vol = vol_values[-1]
        last_vol = vol_values[-2]
        vol_avg = np.average(vol_values[:-1])
        if vol >= last_vol * 2 and vol >= vol_avg * 2:
            features.append(self.VOL_RISE)
        return features
