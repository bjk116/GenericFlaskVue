from flask import Flask, jsonify
from flask import request
from flask import render_template
import os
import click
from flask.cli import with_appcontext
from flask import current_app, g
from flask_cors import CORS
# To get rid of for psm4
import uuid
import mysql.connector
from mysql.connector import errorcode
import json

def create_app(test_config=None):
	#Create and configure app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
			SECRET_KEY='dev',
			DATABASE=os.path.join(app.instance_path, 'PSM4.sqlite')
		)
	# mysql = MySQL(app, host='127.0.0.1', port=3307, user='root', passwd='primary', db='tab')
	cnx = mysql.connector.connect(user="root", password="primary", database="tab", host="localhost", port=3307)

	# For tutorial
	BOOKS = [
    {
    	'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
    	'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
    	'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
	]


	# BE sure to change cors later
	CORS(app, resources={"*": {"origins": "*"}})


	if test_config is None:
		# Load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# Load the test config if pass in
		app.config.from_maping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# Make routes
	@app.route('/')
	def hello_world():
	    return 'Hello, World!'

	def remove_book(book_id):
		for book in BOOKS:
			if book['id'] == book_id:
				BOOKS.remove(book)
				return True
		return False

	# Sample C and R route
	@app.route('/books', methods=['GET', 'POST'])
	def all_books():

		response_object = {'status': 'success'}
		if request.method == 'POST':
			post_data = request.get_json()
			BOOKS.append({
				'id': uuid.uuid4().hex,
				'title': post_data.get('title'),
				'author': post_data.get('author'),
				'read': post_data.get('read')
			})
			response_object['message'] = 'Book added!'
		else:
			response_object['books'] = BOOKS
		return jsonify(response_object)

	@app.route('/timerecords/all', methods=['GET'])
	def get_all_timerecords():
		response_object = {'status': 'success'}

		cnx = mysql.connector.connect(user="root", password="primary", database="tab", host="localhost", port=3307)
		cursor = cnx.cursor()
		query = """
		SELECT DATE_FORMAT(`listlineitems`.`dateEntered`,"%Y-%m-%d") as 'Date Entered',
		CONCAT(`listUsers`.`FirstName`,' ',`listUsers`.`LastName`) as 'Entry Id',
		`listprojects`.`name` as 'Project',
		`listprojects`.`number`'Project #',
		`listactivities`.`name` as 'Activity',
		(CASE `listlineitems`.`type` WHEN 1 THEN `listlineitems`.`qty` WHEN 2 THEN `listlineitems`.`qty` END) as 'Quantity',
		if(view_solinx2.notNeeded = 1, "Not Needed", view_solinx2.number) as 'Sale Order',
		if(view_solinx2.notNeeded = 1,  "------", view_invlinx2.`number`) as 'Invoice',
		if(view_solinx2.notNeeded = 1,  "------",  view_polinx2.`number`) as 'Customer PO'
		FROM `listlineitems` 
		LEFT JOIN `listUsers` ON `listlineitems`.`individualId` = `listUsers`.`idx`
		LEFT JOIN `listprojects` ON `listlineitems`.`parentProjectId` = `listprojects`.`idx`
		LEFT JOIN `listassets` ON `listlineitems`.`parentAssetId` = `listassets`.`idx`
		LEFT JOIN `listareas` ON `listlineitems`.`parentAreaId` = `listareas`.`idx`
		LEFT JOIN `listlocations` ON `listlineitems`.`parentLocationId` = `listlocations`.`idx`
		LEFT JOIN `listcustomers` ON `listlineitems`.`parentCustomerId` = `listcustomers`.`idx`
		LEFT JOIN `listactivities` ON `listactivities`.`idx` = `listlineitems`.`activityCode`
		LEFT JOIN `listexpenseentry` ON (`listexpenseentry`.`idx` = `listlineitems`.`itemId` AND `listlineitems`.`type` = 2)
		LEFT JOIN view_solinx2 ON view_solinx2.idx = listlineitems.idx
		LEFT JOIN view_polinx2 ON view_polinx2.idx = listlineitems.idx
		LEFT JOIN view_invlinx2 ON view_invlinx2.idx = listlineitems.idx
		ORDER BY `listlineitems`.`idx` DESC
		LIMIT 3500
		"""
		cursor.execute(query)
		row_headers=[x[0] for x in cursor.description]

		json_data = []
		for result in cursor:
			json_data.append(dict(zip(row_headers, result)))
		cursor.close()
		cnx.close()
		return json.dumps(json_data)
	
	@app.route('/customers/all', methods=['GET'])
	def get_all_customers():
		response_object = {'status': 'success'}

		cnx = mysql.connector.connect(user="root", password="primary", database="tab", host="localhost", port=3307)
		cursor = cnx.cursor()
		cursor.execute('SELECT idx, name FROM listcustomers ORDER BY name')
	
		data = []
		for idx, name in cursor:
			tempId = str(name) + "/"
			data.append({'id': tempId,  'label':name, 'otherProp': "Customer", 'dbId':idx, "customerId":idx, 'children': None})
		response_object['customers'] = data
		cursor.close()
		cnx.close()
		return jsonify(response_object)
	
	@app.route('/children/<parent_table>/<parent_id>', methods=['GET'])
	def get_children_locations(parent_table, parent_id):
		response_object = {'status': 'success'}
		cnx = mysql.connector.connect(user="root", password="primary", database="tab", host="localhost", port=3307)
		cursor = cnx.cursor()
		otherProp = ''
		query = ''
		
		if parent_table == 'customer':
			query = 'SELECT CONCAT(c.name,"/",l.name,"/") as path, l.idx as idx, l.name as name FROM listlocations l JOIN listcustomers c ON l.parentCustomerId = c.idx WHERE parentCustomerId = %i'%(int(parent_id))
			otherProp = 'Location'
			print("query", query)
		elif parent_table == 'location':
			query = 'SELECT CONCAT(c.name,"/",l.name,"/",a.name,"/") as path, a.idx as idx, a.name as name FROM listareas a JOIN listlocations l ON a.parentLocationId=l.idx JOIN listcustomers c ON l.parentCustomerId = c.idx WHERE parentLocationId = %i'%(int(parent_id))
			otherProp = 'Area'
		elif parent_table == 'area':
			query = 'SELECT CONCAT(c.name,"/",l.name,"/",a.name,"/",ass.name,"/") as path, ass.idx as idx, ass.name as name FROM listassets ass JOIN listareas a ON ass.parentAreaId = a.idx JOIN listlocations l ON a.parentLocationId = l.idx JOIN listcustomers c ON l.parentCustomerId = c.idx WHERE parentAreaId = %i'%(int(parent_id))
			otherProp = 'Asset'
		elif parent_table == 'asset':
			query = 'SELECT CONCAT(c.name,"/",l.name,"/",a.name,"/",ass.name,"/",p.name,"/") as path, p.idx as idx, p.name as name FROM listprojects p JOIN listassets ass ON p.parentAssetId = ass.idx JOIN listareas a ON ass.parentAreaId = a.idx JOIN listlocations l ON a.parentLocationId = l.idx JOIN listcustomers c ON l.parentCustomerId = c.idx WHERE parentAssetId = %i'%(int(parent_id))
			otherProp = 'Project'

		cursor.execute(query)
		data = []
		for path, idx, name in cursor:
			if str(parent_table) == 'customer':
				data.append({'id': path, 'label':name, 'otherProp': otherProp, 'dbId':idx, 'children': None})	
			else:
				data.append({'id': path, 'label':name, 'otherProp': otherProp, 'dbId':idx})

		cursor.close()
		cnx.close()

		print(str(data))

		response_object['payload'] = data
		return jsonify(response_object)

	@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
	def single_book(book_id):
		response_object = {'status': 'success'}
		if request.method == 'PUT':
			post_data = request.get_json()
			remove_book(book_id)
			BOOKS.append({
				'id': uuid.uuid4().hex,
				'title': post_data.get('title'),
				'author': post_data.get('author'),
				'read': post_data.get('read')
			})
			response_object['message'] = 'Book updated!'
		if request.method == 'DELETE':
			remove_book(book_id)
			response_object['message'] = 'Book removed!'
		return jsonify(response_object)

	@app.route('/ping', methods=['GET'])
	def ping():
		print('PONG')
		return jsonify('pong!')

	@app.route('/quotes')
	def viewAllQuotes():
		"""Get and show all quote data on a html page"""
		return 'all quotes here'

	@app.route('/quotes/<int:quote_id>', methods=['GET', 'POST'])
	def handleSingleQuote(quote_id):
		
		# Query database and show single page view of quote
		if request.method == 'POST':
			return 'update the quote here'
		else:
			return render_template('viewSingleQuote.html', quote_id = quote_id)

	@app.route('/quotes/create/<path:subpath>')
	def quotePath(subpath):
		return 'Subpath %s' % subpath

	@app.route('/quotes/toPDF/<int:quote_id>', methods=['GET','POST'])
	def printPDF(quote_id):
		if request.method == 'POST':
			# Create the PDF
			# use that package shithere
			# And upload to server
			pdf = request.files['the_file']
			pdf.save('/NAS/Bay1/Quotes/path.pdf')
		else:
			return "coming soon"

	@click.command('print-quote')
	@with_appcontext
	def printQuote():
		click.echo("printing quote to pdf")

	from . import db
	db.init_app(app)

	return app