'''
Created on 2018年7月17日

@author: ALEX
'''
import analysis.v_shape as v_shape
import analysis.intersection as ins
from analysis.voter import Voter
import data.db_helper as db_helper
from data.model import MA, TradingDataDaily
import numpy as np


class MaVoter(Voter):
    '''
    classdocs
    '''

    def __init__(self, params={}):
        '''
        Constructor
        '''

    def name(self):
        return "MA"
       
    def vote(self, code, day):
        features = []
        values = db_helper.select(self.query_kpi_fn, (code, day, 30, MA))
        if len(values) < 30:
            return features
        values = np.array(values)[::-1]
        ma30_values = np.array(list(map(lambda x:np.float(x.ma_30), values)))
        ma5_values = np.array(list(map(lambda x:np.float(x.ma_5), values)))
        if None in ma30_values:
            return features
        
        is_rebound, break_point = v_shape.positive(ma30_values)
        # 只取5日内的反弹
        if is_rebound and len(ma30_values) - break_point <= 4:
            off_ma_values = ma30_values[break_point:]
            k_values = db_helper.select(self.query_kpi_fn, (code, day, len(off_ma_values), TradingDataDaily))
            k_values = np.array(k_values)[::-1]
            close_values = np.array(list(map(lambda x:np.float(x.close), k_values)))
            
            # 要求开盘价在ma之上
            reb = True
            for i in range(len(off_ma_values)):
                ma_v = off_ma_values[i]
                if ma_v >= close_values[i]:
                    reb = False
                    break;
            if reb:
                features.append(self.REBOUND)
        
        if ins.match(ma5_values[-3:], ma30_values[-3:]) == 1:
            features.append(self.GOOD_CROSS)
            
        return features
    
