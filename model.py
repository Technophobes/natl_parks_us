from sqlalchemy import Integer, Column, String, Float, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker


Base = declarative_base()

# Region is parent of State
class Region(Base):
    __tablename__ = 'Region'
    id = Column(Integer, primary_key=True)
    region_name = Column(String, unique=True)

    def __repr__(self):
        return "<Region(region_name='%s')>" % (self.region_name)

# State is parent of Park
class State(Base):
    __tablename__ = 'State'
# This should be to have the name somewhat unique. Don't think I need that.
#    __table_args__ = (
#        UniqueConstraint('state_id', 'county_name', name='unique_county_state'),
#    )
    id = Column(Integer, primary_key=True)
    state_name = Column(String, unique=True)
    region = relation("Region", backref = "State")
    region_id = Column(Integer, ForeignKey('Region.id'))


    def __repr__(self):
        return "<State(state_name='%s')>" % (self.state_name)


class Park(Base):
    __tablename__ = 'Park'
    # __table_args__ = (
    #     UniqueConstraint('state_id', 'county_name', name='unique_county_state'),
    # )
    id = Column(Integer, primary_key=True)
    park_name = Column(String, unique=True)
    year_founded = Column(Integer)
    state = relation("State", backref = "Park")
    state_id = Column(Integer, ForeignKey('State.id'))


    def __repr__(self):
        return "<Park(park_name='%s')>" % (self.park_name)



# A bunch of stuff to make the connection to the database work.
def dbconnect():
    engine = create_engine('sqlite:///parks.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()