# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月21日

@author: ALEX
'''
import numpy as np


def is_downtrend(values):
    if len(values) < 2:
        return None
    md_idx = (int)(len(values) / 2)
    if np.average(values[:md_idx]) <= np.average(values[md_idx:]):
        return False
    _mean = total = np.max(values)
    for i in range(len(values)):
        total = total + values[i]
        mean = total / (i + 2)
        if mean > _mean:
            return False
        _mean = mean
    return True


def is_uptrend(values):
    if len(values) < 2:
        return None
    md_idx = (int)(len(values) / 2)
    if np.average(values[:md_idx]) >= np.average(values[md_idx:]):
        return False
    _mean = total = np.min(values)
    for i in range(len(values)):
        total = total + values[i]
        mean = total / (i + 2)
        if mean < _mean:
            return False
        _mean = mean
    return True


def is_horizon(values):
    if len(values) < 2:
        return None
    pass


if __name__ == '__main__':
    values = [6, 5, 4, 5, 4, 1]
    r = is_downtrend(values)
    print(r)
    values=values[::-1]
    print(is_uptrend(values))
    pass
