# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月9日

@author: ALEX
'''
import numpy as np
import matplotlib.pyplot as plt
import math


def offset_x(l):
    x = []
    if l % 2 == 0:
        l = (int)(l / 2)
        for i in range(l):
            x.append(0.5 - (l - i))
        for i in range(l):
            x.append(0.5 + i)
        return x
    else:
        print('值的个数必须是双数')
        return None


def match(y, min_slope, max_slope, max_deviation=0.2):
    b = np.average(y)
    x = offset_x(len(y))
    a = np.array(y) / np.array(x)
    a = np.average(a)
    
    if a == 0:
        return False, 0
    
    a = b * 2 / (a * (len(y) + 1)) 
    slope = a / math.sqrt(a * a + 1)
#     print("a=%f,slope=%f" % (a, slope))
    _a = b * 2 / ((len(y) + 1) * a)
    _y = np.array(x) * _a + np.average(y)
    acc = np.mean(np.abs((y - _y) / _y))
#     print("偏差：%f" % (acc))
    matched = False
    if slope >= min_slope and slope <= max_slope and acc <= max_deviation:
        matched = True
    return matched, a
    pass


if __name__ == '__main__':
    y = [10.041, 10.072, 10.096, 10.119, 10.137, 10.161, 10.193, 10.208, 10.187, 10.173, 10.163, 10.153, 10.174, 10.159, 10.15, 10.153, 10.173, 10.183, 10.225, 10.235 ]
#     y = [10.041, 10.072, 10.096, 10.119, 10.137, 10.161]
#     y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     y.reverse()
    matched, a = match(y, -1, 0, 0.2)
    x = offset_x(len(y))
    b = np.average(y)
    a = b * 2 / ((len(y) + 1) * a)
    _y = np.array(x) * a + np.average(y)
#     print("2的平方根：%f" % (math.sqrt(2)))
    plt.figure()
    plt.plot(list(range(len(y))), y, color='b')
    plt.plot(list(range(len(y))), _y, color='r')
    plt.show()
    pass
