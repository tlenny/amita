'''
Created on 2018年7月26日

@author: ALEX
'''
from analysis.voter import Voter
from data.model import DMI  
import data.db_helper as db_helper
import analysis.intersection as ins
import analysis.zero_line as zero_line
import numpy as np


def query_kpi_fn(sess, args):
    code = args[0]
    day = args[1]
    max_result = args[2]
    return sess.query(DMI.time_date, DMI.pdi12, DMI.mdi12, DMI.adx, DMI.adxr).filter(DMI.code == code, DMI.time_date <= day).order_by(DMI.time_date.desc()).limit(max_result)


class DMIVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''
        
    def name(self):
        return 'DMI'
    
    def vote(self, code, day):
        features = []
        values = db_helper.select(query_kpi_fn, (code, day, 30))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        pdi_lines = values[:, 1].astype(float)
        mdi_lines = values[:, 2].astype(float)
        adx_lines = values[:, 3].astype(float)
        adxr_lines = values[:, 4].astype(float)
        
        bt, l = zero_line.breakthrough(adx_lines[-10:], 30)
        if bt and l <= 3:
            features.append(self.BREAK_ZERO)
        
        if ins.match(pdi_lines[-6:], mdi_lines[-6:]) == 1 and ins.match(adx_lines[-3:], adxr_lines[-3:]) == 1:
            features.append(self.GOOD_CROSS)
        
        return features
