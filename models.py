from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine, BIGINT, select, inspect, CHAR
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg2://postgres:klmn@localhost:5432/apartment")
Base = SQLAlchemy()


class A(Base.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def select(cls, *columns):
        return select(*columns if columns else [cls])

    @classmethod
    def create_table(cls, table_name):
        if inspect(engine).has_table(table_name):
            cls.__table__.drop(engine)
        metadata = Base.metadata  # Access the DB Engine
        if not inspect(engine).has_table(table_name):  # If table don't exist, Create.
            metadata.create_all(engine)

    @classmethod
    def select_from_database(cls, *_where):
        with Session(engine) as _session:
            stmt = cls.select()
            if _where:
                stmt = stmt.where(*_where)
            result = _session.scalars(stmt).all()
        return result


class User(A):
    __tablename__ = 'users'
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))
    permission = Column(CHAR(1))

    @classmethod
    def insert_in_database(cls, user):
        super().create_table(cls.__tablename__)
        with Session(engine) as _session:
            user = cls(**user)
            _session.add(user)
            _session.commit()


class Apartment(A):
    __tablename__ = 'apartments'
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
    def insert_in_database(cls, apartments):
        cls.create_table(cls.__tablename__)
        with Session(engine) as _session:
            for item in apartments:
                apartment = cls(**item)
                _session.add(apartment)
                _session.commit()

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
