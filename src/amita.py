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
import analysis.evaluation as ev
import rest.evaluation_rest as rest
from task.pl_job import PlJob
# import ai.learn as ai_learn
# import ai.test as ai_test
import time
import sys


def init_fn(args):
    print('初始化')
    if args.d:
        if args.t == 'ALL':
            init_data.init_all()
        else:
            acqu.pull_data('trading-data-push')
    if args.k is not None:
        print('初始化kpi')
        kpi_names = []
        if args.k == 'ALL':
            kpi_names = init_kpi.all_kpi_names
        else:
            kpi_names = args.k.split(',')
        print(kpi_names)
        for i in range(len(kpi_names)):
            if args.t == 'ALL':
                init_kpi.init_all(kpi_names[i])
            else:
                day = args.t
                init_kpi.init_day(day, kpi_names[i])
    pass


def vote_fn(args):
    ev.elect(args.t, args.l)
    pass


def auto_fn(args):
    now = int(time.time()) 
    time_struct = time.localtime(now) 
    day = time.strftime("%Y-%m-%d", time_struct) 
#     day = '2018-11-05'

    if not init_data.check_done(day):
        print('开始采集交易数据')
        status = acqu.pull_data('trading-data-push')
        if not status:
            print('采集数据失败！')
            sys.exit()
    if not init_data.check_done(day):
        sys.exit()
    print('开始计算指标')
    kpi_names = init_kpi.all_kpi_names
    
    for i in range(len(kpi_names)):
        if not init_kpi.check_done(kpi_names[i], day):
            init_kpi.init_day(day, kpi_names[i])
        pass
    if not ev.check_done(day):
        print('开始评估')     
        ev.elect(day, 20)
    PlJob().run(day)
    pass


def ai_fn(args):
    pass


def eval_fn(args):
    ev.eva(args.t, int(args.c), int(args.d))


def his_fn(args):
    ev.his(args.c, args.t, int(args.d), args.p)
        

def spt_fn(args):
    init_data.init_data(args.f)


def init_kpi_fn(args):
    kpi_names = init_kpi.all_kpi_names
    day = args.d
    for i in range(len(kpi_names)):
        init_kpi.init_day(day, kpi_names[i])
        pass
    print('开始评估')     
    ev.elect(day, 20)
    pass


def web_start_fn(args):
    rest.start()
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='cmd')

    sub_parser = parser.add_subparsers(title='命令列表', help='命令用途')

    init_parser = sub_parser.add_parser('init', help='初始化')
    init_parser.add_argument('-d', action="store_true", default=False, help='交易数据')
    init_parser.add_argument('-k', action="store", help='KPI指标ma,macd,xxx')
    init_parser.add_argument('-t', action="store", default="NOW", help='日期yyyy-mm-dd')
    init_parser.set_defaults(func=init_fn)
    
    dig_parser = sub_parser.add_parser('vote', help='选股')
    dig_parser.add_argument('-t', action="store", default=None, help='日期yyyy-mm-dd')
    dig_parser.add_argument('-l', action="store", default=20, help='最大输出')
    dig_parser.set_defaults(func=vote_fn)
    
    auto_parser = sub_parser.add_parser('auto', help='自动出来：采集、指标、筛选')
    auto_parser.set_defaults(func=auto_fn)
    
    ai_parser = sub_parser.add_parser('ai', help='机器学习')
    ai_parser.add_argument('-l', action="store_true", default=False, help='训练学习')
    ai_parser.add_argument('-t', action="store_true", default=False, help='测试')
    ai_parser.set_defaults(func=ai_fn)
    
    eval_parser = sub_parser.add_parser('eval', help='追踪走势')
    eval_parser.add_argument('-d', action="store", default=5, help='几天内的走势')
    eval_parser.add_argument('-t', action="store", help='评估日期')
    eval_parser.add_argument('-c', action="store", default=20, help='追踪股票个数，按评分从高到低')
    eval_parser.set_defaults(func=eval_fn)
    
    his_parser = sub_parser.add_parser('his', help='追踪走势')
    his_parser.add_argument('-c', action="store", help='股票code')
    his_parser.add_argument('-t', action="store", help='评估日期')
    his_parser.add_argument('-p', action="store_true", default=True, help='向前/向后')
    his_parser.add_argument('-d', action="store", default=10, help='追踪天数')
    his_parser.set_defaults(func=his_fn)

    spt_parser = sub_parser.add_parser('spt', help='补充数据')
    spt_parser.add_argument('-f', action="store", help='数据文件')
    spt_parser.set_defaults(func=spt_fn)

    kpi_parser = sub_parser.add_parser('kpi', help='补充指标')
    kpi_parser.add_argument('-d', action="store", help='日期')
    kpi_parser.set_defaults(func=init_kpi_fn)
    
    web_parser = sub_parser.add_parser('web', help='启动WEB服务')
    web_parser.set_defaults(func=web_start_fn)

    args = parser.parse_args()
    args.func(args)

    pass
