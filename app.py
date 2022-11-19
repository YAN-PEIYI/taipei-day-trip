# coding:utf-8
import os
import mysql.connector
from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key = b"69a2491c26617a5d867681ef213949901b11814b037789b8b311e0fb262d6414"

mydb = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'), 
  user=os.getenv('MYSQL_USER'), 
  passwd=os.getenv('MYSQL_PASSWORD'),
  database=os.getenv('MYSQL_DATABASE'),
)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# 旅遊景點
@app.route('/api/attractions')
def api_attractions():
	try:
		page = request.args.get('page')
		keyword = request.args.get('keyword')
		# print ('page: ', page, ', type: ', type(page))
		# print ('keyword: ', keyword)
		default_num_record = 12
		if page is None:
			page = 0
		offset = int(page) * default_num_record
		# print ('offset: ', offset)		
		# -- next page
		next_page = int(page) + 1
		next_page_offset = int(next_page) * default_num_record

		if keyword:
			mykeyword = '%' + keyword + '%'
			sql = "SELECT * FROM attraction WHERE category = %s OR name LIKE %s LIMIT %s, %s"
			params = (keyword, mykeyword, offset, default_num_record)
			# -- next page
			next_page_params = (keyword, mykeyword, next_page_offset, default_num_record)
		else:
			sql = "SELECT * FROM attraction LIMIT %s, %s"
			params = (offset, default_num_record)
			# -- next page
			next_page_params = (next_page_offset, default_num_record)
		
		cursor = mydb.cursor()
		cursor.execute(sql, params)
		myresult = cursor.fetchall()
		# print (myresult)
		attractions = []
		for x in myresult:
			attraction = {
				"id": x[0],
				"name": x[1],
				"category": x[2],
				"description": x[3],
				"address": x[4],
				"transport": x[5],
				"mrt": x[6],
				"lat": x[7],
				"lng": x[8],
				"images": json.loads(x[9])
			}	
			attractions.append(attraction)
		
		cursor.execute(sql, next_page_params)
		mynextresult = cursor.fetchall()
		if len(mynextresult) == 0:
			next_page = None
		result = {
			'nextPage': next_page,
			'data': attractions
		}
		return jsonify(result)
	except:
		return {
			"error": True,
			"message": "伺服器內部錯誤"
		}, 500	

@app.route('/api/attraction/<int:attractionId>')
def api_attraction(attractionId):
	try:
		# print ('attractionId: ', attractionId)
		cursor = mydb.cursor()
		sql = "SELECT * FROM attraction WHERE id = %s"
		params = (str(attractionId), )
		cursor.execute(sql, params)
		myresult = cursor.fetchone()
		# print (myresult)
		if myresult:
			attraction = {
				"id": myresult[0],
				"name": myresult[1],
				"category": myresult[2],
				"description": myresult[3],
				"address": myresult[4],
				"transport": myresult[5],
				"mrt": myresult[6],
				"lat": myresult[7],
				"lng": myresult[8],
				"images": json.loads(myresult[9])
			}
			result = {
				'data': attraction
			}
			return jsonify(result)
		else:
			return {
				"error": True,
				"message": "景點編號不正確"
			}, 400		
	except:
		return {
			"error": True,
			"message": "伺服器內部錯誤"
		}, 500	

# 旅遊景點分類
@app.route("/api/categories")
def api_categories():
	try:
		cursor = mydb.cursor()
		sql = "SELECT distinct(category) FROM attraction"
		cursor.execute(sql)
		myresult = cursor.fetchall()
		# print (myresult)
		categories = []
		for x in myresult:
			categories.append(x[0])
		result = {
			'data': categories
		}
		return jsonify(result)
	except:
		return {
			"error": True,
			"message": "伺服器內部錯誤"
		}, 500	

app.run(host= '0.0.0.0', port=3000)
