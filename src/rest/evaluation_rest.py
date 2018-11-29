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
import request

# Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
app = Flask(__name__)


@app.route('/eye')
def eye():
	time_date = db_helper.select(query_date,(1))[0][0]
	data = db_helper.select(query_data_fn,(time_date,));
	data = np.array(data)
	text = htmle_head()
	text = text+"<h5>%s</h5>" % time_date
	text = text+"""
		<div>  
   			<ul>  
		"""
	for i in range(len(data)):
		text = text + build_html_with_stock_data(data[i][0],data[i][1],data[i][2])
	text = text + """
		   </ul>  
		 </div> 
		</body>
		</html>
		"""
	return text

@app.route('/detail')
def detail():
	code = request.args.get('code')
	data = db_helper.select(query_detail_data_fn,(code,));
	data = np.array(data)
	text = text+"<h5>%s</h5>" % code
	text = text+"""
		<div>  
   			<ul>  
		"""
	for i in range(len(data)):
		text = text + """
			<li>  
			<a href="/detail?code=%s">%d</a>   
			<h3>%s</h3> 
			<p>%s</p>  
			</li>  
			"""%(data[i][0],data[i][1],data[i][2])
	text = text + """
		   </ul>  
		 </div> 
		</body>
		</html>
		"""
	return text
	pass

def query_date(sess,args):
	return sess.query(Evaluation.time_date).order_by(Evaluation.time_date.desc()).limit(1)

def query_data_fn(sess,args):
	time_date = args[0]
	return sess.query(Evaluation.code,Evaluation.score,Evaluation.feature).filter(Evaluation.time_date == time_date).order_by(Evaluation.score.desc()).limit(10)

def query_detail_data_fn(sess,args):
	code = args[0]
	return sess.query(Evaluation.time_date,Evaluation.score,Evaluation.feature).filter(Evaluation.code == code).order_by(Evaluation.time_date.desc()).limit(20)

def build_html_with_stock_data(code,score,desc):
	text = """
		<li>  
			<a href="/detail?code=%s">%d</a>   
			<h3>%s</h3> 
			<p>%s</p>  
		</li>  
	"""%(code,score,code,desc)
	return text

def htmle_head():
	return """
		<!DOCTYPE html>
		<html>
		<head>
			<title></title>
			<style type="text/css">
		* {margin: 0; padding: 0;}  
		           
		div {  
		   margin: 20px; 
		 }  
		           
		ul {  
		   list-style-type: none;  
		   width: 100%;  
		 }  

		h2 {  
		   font: bold 40px/1.5 Helvetica, Verdana, sans-serif;  
		   text-align: center;
		 }

		h3 {  
		   font: bold 20px/1.5 Helvetica, Verdana, sans-serif;  
		 }  

		h5 {  
		   font: bold 15px/1.5 Helvetica, Verdana, sans-serif;  
		   text-align: right;
		   padding-right: 30px;
		 }

		li a {  
		   float: left;  
		   margin: 0 15px 0 0;  
		   font: bold 30px/1.5 Helvetica, Verdana, sans-serif; 
		   color: red;
		 }  
		           
		li p {  
		   font: 200 12px/1.5 Georgia, Times New Roman, serif;  
		 }  
		           
		li {  
		   padding: 10px;  
		   overflow: auto;  
		 }  
		           
		li:hover {  
		   background: #eee;  
		   cursor: pointer;  
		 } 
			</style>
		</head>

		<body>
		<h2>AMITO</h2>
		"""

def start():
	app.run(host="0.0.0.0", port=80, debug=True)

if __name__ == "__main__":
    # 这种是不太推荐的启动方式，我这只是做演示用，官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
    app.run(host="0.0.0.0", port=80, debug=True)