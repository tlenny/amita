'''
Created on 2018年8月1日

@author: ALEX
'''

from analysis.voter import Voter
from data.model import BOLL, TradingDataDaily
import data.db_helper as db_helper
import numpy as np
import analysis.zero_line as zero_line


class BOLLVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
        
    def name(self):
        return 'BOLL'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(self.query_kpi_fn, (code, day, 30, BOLL))
        k_values = db_helper.select(self.query_kpi_fn, (code, day, 30, TradingDataDaily))
        if len(values) < 30 or len(k_values) < 30 or len(values) != len(k_values):
            return features
        values = np.array(values)[::-1]
        k_values = np.array(k_values)[::-1]
        md_values = np.array(list(map(lambda x:np.float(x.md), values)))
        close_values = np.array(list(map(lambda x:np.float(x.close), k_values)))
        
        bt, l = zero_line.breakthrough(close_values, md_values)
        if bt and l <= 3:
            features.append(self.BREAK_ZERO)
            
        return features
