from model import dbconnect, Region, State, Park
from sqlalchemy import exc

def add_park_from_queue(request_dict):
    session = dbconnect()
    try:
        state_instance = session.query(State).filter(State.id == request_dict["state_id"]).one()
    except:
        return "State does not exist, please add it", 400

    try:
        park = Park()
        park.park_name = request_dict["Unit Name"]
        park.year_founded = request_dict["YearRaw"]
        park.state_id = request_dict["state_id"]
        park.state = state_instance
        session.add(park)
        session.commit()
        # removed json below because this is for flask
        return park.id

    except exc.IntegrityError:
        session.rollback()
        return "already exists", 400