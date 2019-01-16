'''
Created on 2019年1月16日

@author: Administrator
'''
from task.base_job import BaseJob
from portfolio.bias_kdj import BiasKdjAnls

class PlJob(BaseJob):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    def run(self,day):
        BiasKdjAnls().anls(day)
        