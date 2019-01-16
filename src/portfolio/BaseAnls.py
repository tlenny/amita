'''
Created on 2018年12月13日

@author: Administrator
'''

import data.db_helper as db


class BaseAnls(object):
    '''
    classdocs
    '''
    
    def check_done(self, day):
        query_data = db.selectSql('select count(*) from portfolio where type=\'%s\' AND time_date=\'%s\'' % (self.type(), day))
        if len(query_data) == 1:
            if query_data[0][0] > 0:
                return True
        return False
    
    def type(self):
        return ''
    
    def anls(self, day):
        pass

    def save(self, data):
        db.batch_insert(data);
        pass
    
    def __init__(self, params):
        '''
        Constructor
        '''
        
