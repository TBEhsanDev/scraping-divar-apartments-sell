import os
import time
from datetime import timedelta
from pprint import pprint

import psycopg2
import requests
import requests_cache
from sqlalchemy import Column, String, Integer, create_engine, inspect
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, Session

BASE_URL = "https://api.divar.ir/v8/posts-v2/web/"
Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:klmn@localhost:5432/apartment")


class Apartment(Base):
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


def f():
    with open('data.txt', 'a', encoding='utf-8') as f:
        for i in range(10):
            try:
                data = requests.get("https://api.divar.ir/v8/web-search/shiraz/buy-residential")
                _data = data.json()
                for k in range(len(_data["web_widgets"]["post_list"])):
                    if k != len((_data["web_widgets"]["post_list"])):
                        f.write(_data["web_widgets"]["post_list"][k]["data"]["token"] + "\n")
                    else:
                        f.write(_data["web_widgets"]["post_list"][k]["data"]["token"])
            except Exception as e:
                print(e, data)


if not os.path.exists("./data.txt"):
    f()

with open("data.txt", 'r') as f:
    lines = [line[:-1] for line in f]
links = [BASE_URL + line for line in lines]
session = requests_cache.CachedSession('demo_cache', expire_after=timedelta(days=100))
apartments = []
apartment = {'meterage': None, 'made_date': None, 'rooms': None, 'total_price': None, 'price_per_meter': None,
             'advertiser': None, 'floors': None, 'size_of_land': None, 'features': None, 'link': None}
for item in links:
    try:
        j = session.get(item, headers={'User-agent': 'Super Bot Power Level Over 9000'}).json()
        time.sleep(1)
        for s in j.get('sections'):
            if s['section_name'] == 'LIST_DATA':
                for i in s.get('widgets'):
                    if i['widget_type'] == 'GROUP_INFO_ROW':
                        apartment['meterage'] = i.get('data').get('items')[0].get('value')
                        apartment['made_date'] = i.get('data').get('items')[1].get('value')
                        apartment['rooms'] = i.get('data').get('items')[2].get('value')
                    if i['widget_type'] == 'UNEXPANDABLE_ROW':
                        if i['data']['title'] == 'قیمت کل':
                            apartment['total_price'] = i.get('data').get('value')
                        if i['data']['title'] == 'قیمت هر متر':
                            apartment['price_per_meter'] = i.get('data').get('value')
                        if i['data']['title'] == 'آگهی‌دهنده':
                            apartment['advertiser'] = i.get('data').get('value')
                        if i['data']['title'] == 'طبقه':
                            apartment['floors'] = i.get('data').get('value')
                        if i['data']['title'] == "متراژ زمین":
                            apartment['size_of_land'] = i.get('data').get('value')
                    if i['widget_type'] == 'GROUP_FEATURE_ROW':
                        features = []
                        for j in i['data']['items']:
                            features.append(j.get('title'))
                        apartment['features'] = features
                apartment['link'] = item
                apartments.append(apartment)
    except Exception as e:
        pprint(s)


# featurs1 = list()
# featurs2 = list()
# for item in pages:
#     soup = BeautifulSoup(item.content, "html.parser")
#     featurs1.append(soup.findAll("div", class_="kt-group-row-item kt-group-row-item--info-row"))
#     featurs2.append(soup.findAll("div", class_="kt-base-row kt-base-row--large kt-unexpandable-row"))
# apartments_features = list()
# for feature1, feature2, link in zip(featurs1, featurs2, links):
#     apartment = list()
#     apartment.append(int(unidecode(feature1[0].find("span", class_="kt-group-row-item__value").text)))
#     apartment.append(int(unidecode(feature1[1].find("span", class_="kt-group-row-item__value").text)))
#     apartment.append(int(unidecode(feature1[2].find("span", class_="kt-group-row-item__value").text)))
#     apartment.append(int(
#         unidecode((feature2[0].find("p", class_="kt-unexpandable-row__value").text)[:-6]).replace(',', '')))
#     apartment.append(int(
#         unidecode((feature2[1].find("p", class_="kt-unexpandable-row__value").text)[:-6]).replace(',', '')))
#     apartment.append((feature2[-1].find("p", class_="kt-unexpandable-row__value").text))
#     apartment.append(feature1[-3].find("span", class_="kt-group-row-item__value kt-body kt-body--stable").text)
#     apartment.append(feature1[-2].find("span", class_="kt-group-row-item__value kt-body kt-body--stable").text)
#     apartment.append(feature1[-1].find("span", class_="kt-group-row-item__value kt-body kt-body--stable").text)
#     apartment.append(link)
#     apartments_features.append(apartment)
#
# create_apartments_sql = '''create table if not exists apartments(
#      apartment_id serial primary key,
#      meterage int ,
#      made_date int ,
#      rooms int,
#      size_of_land int ,
#      total_price bigint ,
#      price_per_meter bigint ,
#      floors varchar(255) ,
#      advertiser varchar(255),
#      features text[],
#      link varchar(255)
#      )'''
# grant_sql = '''grant all on database apartment to postgres'''
# insert_sql = '''insert into apartments
#     (meterage,made_date,rooms,size_of_land,total_price,price_per_meter,floors,advertiser,features,link)
#     values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
# '''


# noinspection PyShadowingNames
def insert_in_database():
    for item in apartments:
        apartment = Apartment(**item)
        with Session(engine) as _session:
            _session.add(apartment)
            _session.commit()


insert_in_database()
# cursor.execute(create_table_sql)
# print("table created successfully........")
# for item in apartments:
#     cursor.execute(insert_sql, item)
