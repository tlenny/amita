# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月13日

@author: ALEX

'''


def match(x, y):
    '''
            判断两组数的曲线是否相交：
    0-表示不相交
    1-表示x从下往上穿过y
    -1表示x从上往下穿过y
            如果x和y有多个交点，取第一个
    '''
    if len(x) != len(y) and len(x) < 2:
        return 0
    if x[0] == y[0]:
        return 0
    for i in range(len(x) - 1):
        x1, x2, y1, y2 = x[i], x[i + 1], y[i], y[i + 1]
        if x1 < y1 and x2 >= y2:
            return 1
        elif x1 > y1 and x2 <= y2:
            return -1
    return 0


if __name__ == '__main__':
    print(match([3.5,3.4,3],[1,2,3]))
    pass
