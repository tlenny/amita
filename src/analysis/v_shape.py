# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月18日

@author: ALEX
V字型，分为正向V和反向V
正向V：左边下滑，右边上升
反向V：左边上升，右边下滑
返回结果：
    v1:数据是否符合V（正向或反向）字形
    v2:V字的拐点下标
'''
import analysis.trend as trend
import numpy as np


def positive(data):
    size = len(data)
    if size < 4 :
        print('数据必须多余4个')
        return False
    min_idx = 0
    min_v = np.max(data)
    for i in range(size):
        if data[i] <= min_v:
            min_idx = i
            min_v = data[i]
    if min_idx == 0:
        return False, 0
    if min_idx == size - 1:
        return False, size - 1
    left_data = data[0:min_idx + 1]
    right_data = data[min_idx:]
    return trend.is_downtrend(left_data) and trend.is_uptrend(right_data), min_idx


def negative(data, left_size, right_size):
    pass


if __name__ == '__main__':
#     print(positive([8, 7, 6, 5, 4, 3, 4, 6], 6))
    print(positive([10.041, 10.072, 10.096, 10.119, 10.137, 10.161, 10.193, 10.208, 10.187, 10.173, 10.163, 10.153, 10.174, 10.159, 10.15, 10.153, 10.173, 10.183, 10.225, 10.235, 10.247, 10.275, 10.3, 10.32 ]))
    print(positive([6,5,4,3,3,4,5]))
    pass
