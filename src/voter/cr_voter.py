'''
Created on 2018年8月1日

@author: ALEX
'''
from analysis.voter import Voter
from data.model import CR
import data.db_helper as db_helper
import numpy as np


class CRVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
    
    def name(self):
        return 'CR'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(self.query_kpi_fn, (code, day, 30, CR))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        cr_values = np.array(list(map(lambda x:np.float(x.cr), values)))
        
        if cr_values[-1] < 40:
            features.append(self.OVER_SOLD)
            
        return features
