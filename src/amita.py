# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月4日

@author: ALEX
'''
import argparse
import data.init_data as init_data 
import data.data_acquisition as acqu
import kpi.init_kpi as init_kpi
import dig.digger as digger


def init_fn(args):
    print('初始化')
    if args.d:
        if args.t == 'ALL':
            init_data.init_all()
        else:
            acqu.pull_data('trading-data-push')
    if args.k is not None:
        print('初始化kpi')
        kpi_names = args.k.split(',')
        print(kpi_names)
        for i in range(len(kpi_names)):
            if args.t == 'ALL':
                init_kpi.init_all(kpi_names[i])
            else:
                day = args.t
                init_kpi.init_day(day, kpi_names[i])
    pass


def dig_fn(args):
    params = []
    if args.ma:
        params.append(('ma', args.ma))
    if args.macd is not None:
        params.append(('macd', args.ma))
    digger.dig(params)
    pass

def dis_fn(args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='cmd')

    sub_parser = parser.add_subparsers(title='命令列表', help='命令用途')

    init_parser = sub_parser.add_parser('init', help='初始化')
    init_parser.add_argument('-d', action="store_true", default=False, help='交易数据')
    init_parser.add_argument('-k', action="store", help='KPI指标ma,macd,xxx')
    init_parser.add_argument('-t', action="store", help='日期yyyy-mm-dd')
    init_parser.set_defaults(func=init_fn)
    
    dig_parser = sub_parser.add_parser('dig', help='探底')
    dig_parser.add_argument('-ma', action="store_true", default=False, help='MA=20')
    dig_parser.add_argument('-macd', action="store", help='MA=20')
    dig_parser.set_defaults(func=dig_fn)
    
    dis_parser = sub_parser.add_parser('dis', help='图形展现指标')
    dis_parser.add_argument('-l', action="store", default=30, help='最近N天的指标值')
    dis_parser.add_argument('-k', action="store", help='指标列表')
    dis_parser.set_defaults(func=dis_fn)
    
    args = parser.parse_args()
    args.func(args)

    pass
