'''
Created on 2018年12月13日

@author: Administrator
'''

from portfolio.BaseAnls import BaseAnls
import data.db_helper as db_helper

sql = '''
INSERT INTO portfolio(code,time_date,type,grade)
SELECT ev.code,'%s','BIAS_KDJ',1 FROM evaluation ev 
JOIN (SELECT code,bias_24 FROM `bias` WHERE bias_24 < -6 AND time_date='%s') v1 
ON ev.`code` = v1.code 
JOIN (SELECT code,d FROM kdj WHERE time_date='%s' AND d < 16) v2
ON ev.`code` = v2.code 
WHERE ev.time_date='%s' AND ev.feature LIKE '%%KDJ-JC%%';
''' 


class BiasKdjAnls(BaseAnls):
    '''
    classdocs
    '''
    def type(self):
        return 'BIAS_KDJ'

    def anls(self, day):
        if self.check_done(day):
            return
        _sql = sql % (day, day, day, day)
        db_helper.executeSql(_sql)

    def __init__(self):
        '''
        Constructor
        '''


if __name__ == '__main__':
    anls = BiasKdjAnls()
    print(anls.type())
    anls.anls('2019-01-16')
        
