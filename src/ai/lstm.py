'''
Created on 2018年7月31日

@author: ALEX
'''

import tensorflow as tf
import numpy as np
import math

LR = 0.0006
SAVE_STEP = 10


class LSTM(object):
    '''
    classdocs
    '''
    step_size, input_size, rnn_unit, output_size = 40, 1, 256, 1
    saver, path = None, None

    def __init__(self, step_size, input_size, rnn_unit, output_size, save_path):
        '''
        Constructor
        '''
        self.step_size = step_size
        self.input_size = input_size
        self.rnn_unit = rnn_unit
        self.output_size = output_size
        self.path = save_path
        
    def build(self, X):
#         X = tf.placeholder(tf.float32, shape=[None, self.step_size, self.input_size])
        weights = {
             'in':tf.Variable(tf.random_normal([self.input_size, self.rnn_unit])),
             'out':tf.Variable(tf.random_normal([self.rnn_unit, 1]))
            }
        biases = {
            'in':tf.Variable(tf.constant(0.1, shape=[self.rnn_unit, ])),
            'out':tf.Variable(tf.constant(0.1, shape=[1, ]))
           }
#         batch_size = tf.shape(X)[0]
#         time_step = tf.shape(X)[1]
#         w_in = weights['in']
#         b_in = biases['in']  
#         input_rnn = tf.reshape(X, [-1, self.input_size])  # 需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
#         input_rnn = tf.matmul(input_rnn, w_in) + b_in
#         input_rnn = tf.reshape(input_rnn, [-1, time_step, self.rnn_unit])  # 将tensor转成3维，作为lstm cell的输入
#         cell = tf.nn.rnn_cell.BasicLSTMCell(self.rnn_unit)
#         init_state = cell.zero_state(batch_size, dtype=tf.float32)
#         output_rnn, final_states = tf.nn.dynamic_rnn(cell, input_rnn, initial_state=init_state, dtype=tf.float32)  # output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
#         output = tf.reshape(output_rnn, [-1, self.rnn_unit])  # 作为输出层的输入
        output = tf.placeholder(tf.float32, [None, self.rnn_unit])
        w_out = weights['out']
        b_out = biases['out']
#         pred = tf.matmul(output, w_out) + b_out
        pred = tf.nn.softmax(tf.matmul(output, w_out) + b_out)
#         pred = RNN(X, weights, biases)
        return pred
        
    def restore(self):
        self.build()
        self.saver = tf.train.Saver(tf.global_variables(), max_to_keep=15)
        with tf.Session() as sess:
            try:
                self.saver.restore(sess, tf.train.latest_checkpoint(self.path))
                print("成功读取模型文件")
            except Exception:
                print("没有模型文件")
    
    def learn(self, times, x, y, batch_size=800):
        X = tf.placeholder(tf.float32, shape=[None, self.step_size, self.input_size])
        Y = tf.placeholder(tf.float32, shape=[None])
#         Y = tf.placeholder(tf.float32, shape=[None, self.step_size, self.output_size])
        pred = self.build(X)
        # 分类学习
#         cost = tf.reduce_mean(tf.square(y - pred))
#         cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
#         tf.train.AdamOptimizer(LR).minimize(cost)
        cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(pred), reduction_indices=1))
        tf.train.AdamOptimizer(LR).minimize(cost)
#         optimizer = tf.train.GradientDescentOptimizer(LR).minimize(cost)
        correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        # end 分类学习
        
#         loss = tf.reduce_mean(tf.square(tf.reshape(pred, [-1]) - tf.reshape(Y, [-1])))
#         train_op = tf.train.AdamOptimizer(LR).minimize(loss)
        self.saver = tf.train.Saver(tf.global_variables(), max_to_keep=15)

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            try:
                self.saver.restore(sess, tf.train.latest_checkpoint(self.path))
                print("成功读取模型文件")
            except Exception:
                print("没有模型文件")
            fail = 0
            for i in range(times):
                loss_values = []
                accuracy_rate = None
                batch_num = math.ceil(len(x) / batch_size)
                for num in range(batch_num):
                    _x = x[num:(num + 1) * batch_size]
                    _y = y[num:(num + 1) * batch_size]
                    try:
                        accuracy_rate = sess.run(accuracy, feed_dict={X:_x, Y:_y})
#                         _, loss_ = sess.run([train_op, loss], feed_dict={X:_x, Y:_y})
#                         loss_values.append(loss)
                    except Exception as e:
                        print(e)
                        fail = fail + 1
                if (i + 1) % SAVE_STEP == 0:
                    self.saver.save(sess, self.path)
#                     print('完成：%d次，失败：%d次，平均误差：%.6f' % ((i + 1), fail, np.mean(loss_values, axis=0)))
                    print('完成：%d次，失败：%d次，准确率：%.6f' % ((i + 1), fail, accuracy_rate))
        
    def test(self, x):
        X = tf.placeholder(tf.float32, shape=[None, self.step_size, self.input_size])
        pred, _ = self.build(X)
        self.saver = tf.train.Saver(tf.global_variables(), max_to_keep=15)

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            try:
                self.saver.restore(sess, tf.train.latest_checkpoint(self.path))
                print("成功读取模型文件")
            except Exception:
                print("没有模型文件")
                return None
            test_y = []
            for step in range(len(x)):
                prob = sess.run(pred, feed_dict={X:[x[step]]})   
                predict = prob.reshape((-1))
                test_y.extend(predict)
            return test_y
        
