import psycopg2
from sqlalchemy import inspect

from models import Apartment, engine, Base


def create_db():
    conn = None
    try:
        conn = psycopg2.connect(
            database="postgres", user='postgres', password='klmn', host='127.0.0.1', port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'apartment'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE apartment')

        conn = psycopg2.connect(
            database="apartment", user='postgres', password='klmn', host='127.0.0.1', port='5432'
        )
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


def create_table():
    if inspect(engine).has_table("apartments"):
        Apartment.__table__.drop(engine)
    metadata = Base.metadata  # Access the DB Engine
    if not inspect(engine).has_table("apartments"):  # If table don't exist, Create.
        metadata.create_all(engine)


create_db()
create_table()
