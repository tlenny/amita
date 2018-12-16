'''
Created on 2018年12月13日

@author: Administrator
'''

import data.db_helper as db

class BaseAnls(object):
    '''
    classdocs
    '''
    
    def anls(self, day):
        pass

    def save(self,data):
        db.batch_insert(data);
        pass
    
    def __init__(self, params):
        '''
        Constructor
        '''
        