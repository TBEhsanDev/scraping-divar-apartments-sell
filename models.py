from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, inspect, create_engine, BIGINT
from sqlalchemy.dialects.postgresql import ARRAY

engine = create_engine("postgresql+psycopg2://postgres:klmn@localhost:5432/apartment")
Base = SQLAlchemy()


class Apartment(Base.Model):
    __tablename__ = 'apartments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    meterage = Column(Integer)
    made_date = Column(Integer)
    rooms = Column(Integer)
    size_of_land = Column(Integer)
    total_price = Column(BIGINT)
    price_per_meter = Column(BIGINT)
    floors = Column(Integer)
    advertiser = Column(String(255))
    features = Column(ARRAY(String(255)))
    link = Column(String(255))
    description = Column(String(1000))


Base.metadata.create_all(engine, checkfirst=True)


def create_table():
    if inspect(engine).has_table("apartments"):
        Apartment.__table__.drop(engine)
    metadata = Base.metadata  # Access the DB Engine
    if not inspect(engine).has_table("apartments"):  # If table don't exist, Create.
        metadata.create_all(engine)
