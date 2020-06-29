# This api will import data to the database

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from model import dbconnect, Region, State, Park
from sqlalchemy import exc
from redis import Redis
from rq import Queue
from park_queue import add_park_from_queue


app = Flask(__name__)
CORS(app)
# https://python-rq.org/
q = Queue('parks', connection=Redis())

@app.route('/region', methods=['POST'])
def add_region():
	session = dbconnect()
	request_dict = request.get_json()
	try:
		region_instance = Region()
		region_instance.region_name = request_dict["Region"]
		session.add(region_instance)
		session.commit()
		return jsonify(region_instance.id)
	except exc.IntegrityError:
		session.rollback()
		return "already exists", 400

@app.route('/station',  methods=['POST'])
def add_station():
	session = dbconnect()
	request_dict = request.get_json()
	try:
		# Check if region is existing. Why are we doing this? We do nothing with the result.
		# Make sure that we dont try and add a station without a region
		region_instance = session.query(Region).filter(Region.id == request_dict["region_id"]).one()
	except exc.IntegrityError:
		return "region does not exist", 400
	# Add the data to the queue
	q.enqueue(add_station_from_queue, request_dict)
	return "OK", 200

@app.route('/region/<search_term>', methods=['GET'])
def get_region(search_term):
	session = dbconnect()
	try:
		region_instance = session.query(Region).filter(Region.region_name == search_term).one()
		return jsonify(region_instance.id), 200
	except:
		return "Region doesn't exist in database", 400

@app.route('/station/<search_term>', methods=['GET'])
def get_station(search_term):
	session = dbconnect()
	return_list = []
	if search_term == "all":
		for row in session.query(Station).all():
			row_dict = row.__dict__
			row_dict.pop("_sa_instance_state")
			return_list.append(row_dict)
	else:
		for row in session.query(Station).filter(Station.station_name == search_term).all():
			row_dict = row.__dict__
			row_dict.pop("_sa_instance_state")
			return_list.append(row_dict)
	return jsonify(return_list)



# This provides the error message on the url
if __name__ == '__main__':

	app.run(debug=True)