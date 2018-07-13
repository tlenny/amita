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


def match(y, min_slope, max_slope, max_deviation):
    b = np.average(y)
    x = offset_x(len(y))
    a = np.array(y) / np.array(x)
    a = np.average(a)
    
    a = b * 2 / (a * (len(y) + 1)) 
    slope = a / math.sqrt(a * a + 1)
#     print("a=%f,slope=%f" % (a, slope))
    _a = b * 2 / ((len(y) + 1) * a)
    _y = np.array(x) * _a + np.average(y)
    acc = np.mean(np.abs((y - _y) / _y))
#     print("偏差：%f" % (acc))
    matched = False
    if slope >= min_slope and slope <= max_slope and acc <= 0.2:
        matched = True
    return matched, a
    pass


if __name__ == '__main__':
    y = [10, 18, 33, 39, 51, 60, 72, 76, 91, 99]
#     y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y.reverse()
    matched, a = match(y, 0, 1, 1)
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
