'''
Created on 2018年7月19日

@author: ALEX
'''


class Progress(object):
    '''
    进度条
    '''
    total, step, last = 100, 5, -1

    def __init__(self, total=100, step=10):
        '''
        total:进度总长度
        step：进度输出的步长1-100
        '''
        self.total = total
        self.step = step
        
    def log(self, size):
        _prog = (int)((size) / self.total * 100)
        if _prog % self.step == 0:
            if _prog > self.last:
                self.last = _prog
                print('%d%%\t%s%s' % (_prog, _prog * '*', (int)(100 - _prog) * '-'))
    
    def setting(self, total=100, step=10):
        self.total = total
        self.step = step
        self.last = -1
