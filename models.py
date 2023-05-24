from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, inspect, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base


engine = create_engine("postgresql+psycopg2://postgres:klmn@localhost:5432/apartment")
Base=SQLAlchemy()

class Apartment(Base.Model):
    __tablename__ = 'apartments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    meterage = Column(String(255))
    made_date = Column(String(255))
    rooms = Column(String(255))
    size_of_land = Column(String(255))
    total_price = Column(String(255))
    price_per_meter = Column(String(255))
    floors = Column(String(255))
    advertiser = Column(String(255))
    features = Column(ARRAY(String(255)))
    link = Column(String(255))


Base.metadata.create_all(engine, checkfirst=True)


def create_table():
    if inspect(engine).has_table("apartments"):
        Apartment.__table__.drop(engine)
    metadata = Base.metadata  # Access the DB Engine
    if not inspect(engine).has_table("apartments"):  # If table don't exist, Create.
        metadata.create_all(engine)
