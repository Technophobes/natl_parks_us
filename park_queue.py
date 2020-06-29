from model import dbconnect, Region, State, Park
from sqlalchemy import exc

def add_park_from_queue(request_dict):
    session = dbconnect()
    try:
        state_instance = session.query(State).filter(State.id == request_dict["state_id"]).one()
    except:
        # wrong. Not sure why this was wrong before? Json stuff only
        return "State does not exist, please add it", 400

    try:
        park = Park()
        park.park_name = request_dict["Park"]
        park.state = state_instance
        session.add(park)
        session.commit()
        # removed json below because this is for flask
        return park.id

    except exc.IntegrityError:
        session.rollback()
        # wrong
        return "already exists", 400