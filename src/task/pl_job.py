'''
Created on 2019年1月16日

@author: Administrator
'''
from task.base_job import BaseJob
from portfolio.bias_kdj import BiasKdjAnls

anls_factory = [BiasKdjAnls()]

class PlJob(BaseJob):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def run(self,day):
        for i in range(len(anls_factory)):
            a = anls_factory[i]
            print('分析【%s】'%(a.type(),))
            a.anls(day)
            print('分析【%s】结束'%(a.type(),))

if __name__ == '__main__':
    PlJob().run('2019-01-21')
    pass