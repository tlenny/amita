# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月3日

@author: ALEX
'''


class DbProp(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    #mysql+pymysql
#     url = 'mysql+mysqlconnector://root:yuXi@0108@localhost:3306/amita?charset=utf8mb4'
    url = 'mysql+mysqlconnector://root:yuXi@0108@47.94.111.188:3306/amita?charset=utf8mb4'
    encoding = 'utf8mb4'
    echo_flag = True
    
