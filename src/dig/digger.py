'''
Created on 2018年7月11日

@author: ALEX
'''

import kpi.ma.ma_as as ma

def get_int_param_value(args, index):
    arr = args.split(',')
    if len(arr) > index:
        return int(arr[index])
    else:
        return None


def join(a, b):
    if a is None:
        return b
    else:
        return a & b


def dig(params):
    rst = None
    for i in range(len(params)):
        name = params[i][0]
        args = params[i][1]
        if name == 'ma':
            r = ma.dig()
            rst = join(rst, set(r))
        else:
            print('暂不支持：%s' % name)
    print('**********************************************************************')
    print(rst)
    print('**********************************************************************')
    pass


if __name__ == '__main__':
    a = set([1, 2, 3])
    b = set([2, 3, 4])
    c = a & b
    print(c)
    pass
