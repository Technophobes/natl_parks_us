import requests
import json
import pandas as pd


df = pd.read_csv("parks_short.csv")


def wrangle(input_object):
    input_dict = input_object.to_dict()
    # This adds the entry's Region
    pload_region = {"Region": input_dict["Region"]}
    region_request = requests.get("http://127.0.0.1:5000/region/{}".format(input_dict["Region"]))
    if region_request.status_code == 400:
        region_request = requests.post("http://127.0.0.1:5000/region" , json=pload_region)
    input_dict["region_id"] = region_request.text

    # THIS DOESN'T SEEM TO MATTER. WHY?!
    # state_request = requests.get("http://127.0.0.1:5000/state/{}".format(input_dict["State"]))
    # if state_request.status_code == 400:
    #     state_request = requests.post("http://127.0.0.1:5000/state" , json=pload_state)
    # input_dict["state_id"] = state_request.text

    # This adds the entry's State
    # Why don't i need to be more specific? Even if the region already exists, that doesn't mean the state does
    # pload_state = {"State": input_dict["State"]}
    requests.post("http://127.0.0.1:5000/state" , json=input_dict)

    requests.post("http://127.0.0.1:5000/park" , json=input_dict)



df.apply(wrangle, axis=1)