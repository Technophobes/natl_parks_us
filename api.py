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

@app.route('/state', methods=['POST'])
def add_state():
	session = dbconnect()
	request_dict = request.get_json()
	try: 
		region_instance = session.query(Region).filter(Region.id == request_dict["region_id"]).one()
	except: 
		return "Region does not exist, please add it", 400

	try:
		state_instance = State()
		state_instance.state_name = request_dict["State"]
		state_instance.region_id = request_dict["region_id"]
		session.add(state_instance)
		session.commit()
		return jsonify(state_instance.id)
	except exc.IntegrityError:
		session.rollback()
		return "already exists", 400

@app.route('/park',  methods=['POST'])
def add_park():
	session = dbconnect()
	request_dict = request.get_json()
	try:
		# Check if state (parent of park) is existing so api doesn't add park without state (which will only be added with its parent Region)
		state_instance = session.query(State).filter(State.id == request_dict["state_id"]).one()
	except exc.IntegrityError:
		return "State does not exist", 400
	# Add the data to the queue
	q.enqueue(add_park_from_queue, request_dict)
	return "OK", 200

@app.route('/region/<search_term>', methods=['GET'])
def get_region(search_term):
	session = dbconnect()
	try:
		region_instance = session.query(Region).filter(Region.region_name == search_term).one()
		return jsonify(region_instance.id), 200
	except:
		return "Region doesn't exist in database", 400

@app.route('/state/<search_term>', methods=['GET'])
def get_state(search_term):
	session = dbconnect()
	return_list = []
	if search_term == "all":
		for row in session.query(State).all():
			row_dict = row.__dict__
			row_dict.pop("_sa_instance_state")
			return_list.append(row_dict)
	else:
		for row in session.query(State).filter(State.state_name == search_term).all():
			row_dict = row.__dict__
			row_dict.pop("_sa_instance_state")
			return_list.append(row_dict)
	return jsonify(return_list)

@app.route('/park/<search_term>', methods=['GET'])
def get_park(search_term):
	session = dbconnect()
	return_list = []
	if search_term == "all":
		for row in session.query(Park).all():
			row_dict = row.__dict__
			row_dict.pop("_sa_instance_state")
			return_list.append(row_dict)
	else:
		for row in session.query(Park).filter(Park.park_name == search_term).all():
			row_dict = row.__dict__
			row_dict.pop("_sa_instance_state")
			return_list.append(row_dict)
	return jsonify(return_list)

# Patch or Put to update a park
# https://devcamp.com/trails/python-api-development-with-flask/campsites/hello-flask/guides/guide-building-update-action-put-request-flask
@app.route('/park/update/<search_term>',  methods=['PUT'])
def update_park(search_term):
    session = dbconnect()
    park = Park.query.get(search_term)
    park_name = request.json["Unit Name"]

    park.park_name = park_name

    db.session.commit()
    return "Park has been updated", 200


# Delete Park
# https://devcamp.com/trails/python-api-development-with-flask/campsites/279/guides/how-to-build-delete-api-endpoint-flask-project-summary
@app.route('/park/delete/<search_term>',  methods=['DELETE'])
def delete_park(search_term):
    session = dbconnect()
    park = Park.query.get(search_term)
    db.session.delete(park)
    db.session.commit()
    return "Park has been deleted", 200


# This provides the error message on the url
if __name__ == '__main__':

	app.run(debug=True)