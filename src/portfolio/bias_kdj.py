'''
Created on 2018年12月13日

@author: Administrator
'''

from portfolio.BaseAnls import BaseAnls

sql = '''
SELECT ev.code FROM evaluation ev 
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

    def anls(self, day):
        BaseAnls.anls(self, day)

    def __init__(self, params):
        '''
        Constructor
        '''


if __name__ == '__main__':
    day = '2018-12-13'
    print(sql % (day, day, day))
        
