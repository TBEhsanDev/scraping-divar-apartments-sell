import psycopg2
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

from models import Apartment



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




create_db()

