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
    url = 'mysql+mysqlconnector://root:root@localhost:3306/amita?charset=utf8mb4'
    encoding = 'utf8mb4'
    echo_flag = True
    
