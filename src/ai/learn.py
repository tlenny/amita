'''
Created on 2018年8月2日

@author: ALEX
'''
from ai.lstm import LSTM
import ai.data_query as query
import numpy as np


def learning(code):
    print('开始学习%s' % code)
    time_step = 40
    rnn_unit = 256
    output_size = 1
    input_size = query.get_select_fields_count()
    lstm = LSTM(time_step, input_size, rnn_unit, output_size, 'D:/tomorrow/data/ai/model/%s/' % code)
    print('开始准备学习数据...')
    x, y = query.query_data(code, None, '2018-03-31')
    print('获取数据%d条' % len(x))
    std_x = np.std(x)
    mean_x = np.mean(x)
    x = (x - mean_x) / std_x
#     std_y = np.std(y)
#     mean_y = np.mean(y)
#     y = (y - mean_y) / std_y
    data_x, data_y = [], []
    for i in range(len(x) - time_step + 1):
        data_x.append(np.array(x[i:i + time_step], dtype=np.float32)) 
#         data_y.append(np.array(y[i:i + time_step], dtype=np.float32)) 
        data_y.append(np.array(y[i:i + time_step], dtype=np.float32)[-1, 0]) 
    print('开始学习...')
    lstm.learn(1000000, data_x, data_y)

    
if __name__ == '__main__':
    learning('600004')
    pass
