from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine, BIGINT, select, inspect
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Session

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
    floors = Column(String(255))
    advertiser = Column(String(255))
    features = Column(ARRAY(String(255)))
    link = Column(String(255))
    description = Column(String(5000))

    @classmethod
    def select(cls, *columns):
        return select(*columns if columns else [cls])

    @classmethod
    def create_table(cls):
        if inspect(engine).has_table("apartments"):
            Apartment.__table__.drop(engine)
        metadata = Base.metadata  # Access the DB Engine
        if not inspect(engine).has_table("apartments"):  # If table don't exist, Create.
            metadata.create_all(engine)

    @classmethod
    def insert_in_database(cls, apartments):
        cls.create_table()
        with Session(engine) as _session:
            for item in apartments:
                apartment = cls(**item)
                _session.add(apartment)
                _session.commit()

    @classmethod
    def select_from_database(cls):
        with Session(engine) as _session:
            apartments = _session.scalars(cls.select()).all()
        return apartments

    @classmethod
    def query_result_to_list_of_dict(cls, apartments):
        result = []
        for i, item in enumerate(apartments):
            a = item.__dict__
            del a['_sa_instance_state']
            del a['id']
            a['count'] = i
            des = a.pop('description')
            des = ("description", des)
            l = list(a.items())
            l.append(des)
            a = dict(l)
            result.append(a)
        return result
