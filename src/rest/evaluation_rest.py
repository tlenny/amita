# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年11月24日

@author: ALEX
'''
from flask import Flask
from data.model import Evaluation
import data.db_helper as db_helper
import numpy as np

# Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
app = Flask(__name__)


@app.route('/eye')
def eye():
	time_date = db_helper.select(query_date,(1))[0][0]
	data = db_helper.select(query_data_fn,(time_date));
	data = np.array(data)
	text = """
		<html>
		<head>
		</head>
		<body>
		<h2 align="center" style="color: red;">
			智 眼
		</h2>
		<div width="90%" align="right" style="font-size: 14px;color: #434343;">%s</div>
		<br>
		<table width="100%" cellspacing="0">
		"""%(time_date,)
	for i in range(len(data)):
		text = text + build_html_with_stock_data(data[i][0],data[i][1],data[i][2])
	text = text + """
		</table>
		</body>
		</html>
		"""
	return text

def query_date(sess,args):
	return sess.query(Evaluation.time_date).order_by(Evaluation.time_date.asc()).limit(1)

def query_data_fn(sess,args):
	time_date = args[0]
	return sess.query(Evaluation.code,Evaluation.score,Evaluation.feature).filter(Evaluation.time_date == time_date).order_by(Evaluation.score.asc()).limit(10)



def build_html_with_stock_data(code,score,desc):
	text = """
	<tr style="background-color: #f9ac9e;">
		<td align="left" style="font-size: 16px;color: red; font-weight: bold; ">%s</td>
		<td align="right" style="font-size: 16px;color: red">%s</td>
	</tr>
	<tr style="background-color: #cccccc;">
		<td colspan="2" align="right" style="font-size: 14px; color:black">%s</td>
	</tr>
	"""%(code,score,desc)
	return text

def start():
	app.run(host="0.0.0.0", port=80, debug=True)

if __name__ == "__main__":
    # 这种是不太推荐的启动方式，我这只是做演示用，官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
    app.run(host="0.0.0.0", port=80, debug=True)