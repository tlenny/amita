'''
Created on 2018年7月29日

@author: ALEX
'''
from analysis.voter import Voter
from data.model import DMA
import data.db_helper as db_helper
import analysis.intersection as ins
import analysis.zero_line as zero_line
import numpy as np


class DMAVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
    
    def name(self):
        return 'DMA'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(self.query_kpi_fn, (code, day, 30, DMA))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        dma_values = np.array(list(map(lambda x:np.float(x.dma), values)))
        ama_values = np.array(list(map(lambda x:np.float(x.ama), values)))
        
        bt, l = zero_line.breakthrough(dma_values[-10:])
        if bt and l <= 3:
            features.append(self.BREAK_ZERO)
        
        if ins.match(dma_values[-3:], ama_values[-3:]) == 1:
            features.append(self.GOOD_CROSS)
        return features
        
