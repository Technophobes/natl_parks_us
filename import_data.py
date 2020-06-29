import requests
import json
import pandas as pd


df = pd.read_csv("parks_short.csv")


def wrangle(input_object):
	input_dict = input_object.to_dict()

	pload_region = {"Region": input_dict["Region"]}

	region_request = requests.get("http://127.0.0.1:5000/region/{}".format(input_dict["Region"]))
	if region_request.status_code == 400:
		region_request = requests.post("http://127.0.0.1:5000/region" , json=pload_region)
	input_dict["region_id"] = region_request.text

	pload_state = {"State": input_dict["State"]}

	state_request = requests.get("http://127.0.0.1:5000/state/{}".format(input_dict["State"]))
	if state_request.status_code == 400:
		state_request = requests.post("http://127.0.0.1:5000/state" , json=pload_state)
	input_dict["state_id"] = state_request.text

	requests.post("http://127.0.0.1:5000/park" , json=input_dict)


df.apply(wrangle, axis=1)