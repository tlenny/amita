'''
Created on 2018年7月24日

@author: ALEX
'''

import numpy as np
from numpy import ndarray


def under_zero(values, zero_lines):
    sub = values - zero_lines
    if np.average(sub) >= 0:
        return False
    under = list(filter(lambda x:x < 0, sub))
    return len(under) / len(values) >= 0.9


def breakthrough(values, zero=0):
    '''
            试图寻找零线的突破点，返回
    V1：是否存在突破
    V2：突破后的数据长度
    '''
    ln = len(values)
    if ln <= 1 :
        return False, -1
    point = -1
    
    for i in range(ln):
        z = None
        if isinstance(zero,ndarray):
            z = zero[i]
        else:
            z = zero
        if values[ln - i - 1] < z:
            point = ln - i
            break;
    if point == ln or point == 0:
        return False, -1
    
    under_zero_value = values[:point]
    std_zero_value = None
    if isinstance(zero,ndarray):
        std_zero_value = zero[:point]
    else:
        std_zero_value = np.full((len(under_zero_value)),zero)
        
    if under_zero(under_zero_value, std_zero_value):
        return True, ln - point
    else:
        return False, -1
    pass


if __name__ == '__main__':
    print(type(0))
    print(isinstance(0,float))
    print(type(np.zeros(12)))
    print(isinstance(np.zeros(12), ndarray))
    print(np.full((5), 3))
    print(breakthrough([-1, -2, 1, -1, -3, -2, -1, -1, -1, -1, 0.5, 1.2], np.full((12),1)))
    pass
