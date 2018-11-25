'''
Created on 2018年7月29日

@author: ALEX
'''

from analysis.voter import Voter
from data.model import EMV, TradingDataDaily
import data.db_helper as db_helper
import analysis.trend as trend
import analysis.zero_line as zero_line
import numpy as np


class EMVVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
    
    def name(self):
        return 'EMV'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(self.query_kpi_fn, (code, day, 30, EMV))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        emv_values = np.array(list(map(lambda x:np.float(x.emv), values)))
        if trend.is_uptrend(emv_values[-10:]):
            k_values = db_helper.select(self.query_kpi_fn, (code, day, 10, TradingDataDaily))
            if len(k_values) == 10:
                k_values = np.array(k_values)[::-1]
                close_values = np.array(list(map(lambda x:np.float(x.close), k_values)))
                if trend.is_downtrend(close_values):
                    features.append(self.BOTTOM_DEVIATION)
        
        bt, l = zero_line.breakthrough(emv_values[-10:])
        if bt and l <= 3:
            features.append(self.BREAK_ZERO)
    
        return features