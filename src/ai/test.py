'''
Created on 2018年7月31日

@author: ALEX
'''
from ai.lstm import LSTM
import ai.data_query as query
import numpy as np
import matplotlib.pyplot as plt
import math


def testing(code):
    print('开始%s' % code)
    time_step = 40
    rnn_unit = 256
    output_size = 1
    input_size = query.get_select_fields_count()
    lstm = LSTM(time_step, input_size, rnn_unit, output_size, 'D:/tomorrow/data/ai/model/%s/' % code)
    print('开始准备测试数据...')
    x, y = query.query_data(code, '2018-01-01', '2018-04-30')
    print('获取数据%d条' % len(x))
    y = np.array(y)
    
    size = (len(x) // time_step) * time_step
    x = x[-size:]
    y = y[-size:]
    
    std_x = np.std(x)
    mean_x = np.mean(x)
    x = (x - mean_x) / std_x
    data_x, data_y = [], []
    for i in range(len(x) // time_step):
        data_x.append(np.array(x[i * time_step:(i + 1) * time_step], dtype=np.float32)) 
        data_y.extend(np.array(y[i * time_step:(i + 1) * time_step, 0], dtype=np.float32)) 
    print('开始验证...')
    test_y = lstm.test(data_x)
    if test_y == None:
        print('测试失败')
    
#     std_y = np.std(data_y)
#     mean_y = np.mean(data_y)
#     data_y = (data_y - mean_y) / std_y
#     test_y = np.array(test_y) * np.float(std_y) + mean_y
    test_y = np.round(test_y, 4)
    
    plt.figure()
    plt.plot(list(range(len(test_y))), test_y, color='b')
    plt.plot(list(range(len(data_y))), data_y, color='r')
    plt.show()
    print('完毕')

    
if __name__ == '__main__':
#     testing('600004')
    print(math.ceil(60 / 40))
    print(math.ceil(80 / 40))
    print(math.ceil(81 / 40))
    pass
