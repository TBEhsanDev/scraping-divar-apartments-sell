import os
from datetime import timedelta

import psycopg2
import requests
import requests_cache
from bs4 import BeautifulSoup
from unidecode import unidecode

BASE_URL = "https://divar.ir/v/"


def f():
    last_date = 1669189620361141
    with open('data.txt', 'a', encoding='utf-8') as f:
        for i in range(10):
            data = requests.post("https://api.divar.ir/v8/web-search/6/apartment-sell",
                                 json={"json_schema": {"category": {"value": "apartment-sell"}, "cities": ["6"]},
                                       "last-post-date": last_date})
            j = data.json()
            last_date = j["last_post_date"]
            for i in range(len(j["web_widgets"]["post_list"])):
                if i != len((j["web_widgets"]["post_list"])):
                    f.write(j["web_widgets"]["post_list"][i]["data"]["token"] + "\n")
                else:
                    f.write(j["web_widgets"]["post_list"][i]["data"]["token"])


isExist = os.path.exists("./data.txt")
if not isExist:
    f()

with open("data.txt", 'r') as f:
    lines = [line[:-1] for line in f]
links = [BASE_URL + line for line in lines]
session = requests_cache.CachedSession('demo_cache', expire_after=timedelta(days=100))
pages = list()
for item in links:
    pages.append(session.get(item, headers={'User-agent': 'Super Bot Power Level Over 9000'}))
featurs1 = list()
featurs2 = list()
for item in pages:
    soup = BeautifulSoup(item.content, "html.parser")
    featurs1.append(soup.findAll("div", class_="kt-group-row-item"))
    featurs2.append(soup.findAll("div", class_="kt-base-row kt-base-row--large kt-unexpandable-row"))
apartments_features = list()
for feature1, feature2, link in zip(featurs1, featurs2, links):
    apartment = list()
    apartment.append(int(unidecode(feature1[0].find("span", class_="kt-group-row-item__value").text)))
    apartment.append(int(unidecode(feature1[1].find("span", class_="kt-group-row-item__value").text)))
    apartment.append(int(unidecode(feature1[2].find("span", class_="kt-group-row-item__value").text)))
    apartment.append(int(
        unidecode((feature2[0].find("p", class_="kt-unexpandable-row__value").text)[:-6]).replace(',', '')))
    apartment.append(int(
        unidecode((feature2[1].find("p", class_="kt-unexpandable-row__value").text)[:-6]).replace(',', '')))
    apartment.append((feature2[-1].find("p", class_="kt-unexpandable-row__value").text))
    apartment.append(feature1[-3].find("span", class_="kt-group-row-item__value kt-body kt-body--stable").text)
    apartment.append(feature1[-2].find("span", class_="kt-group-row-item__value kt-body kt-body--stable").text)
    apartment.append(feature1[-1].find("span", class_="kt-group-row-item__value kt-body kt-body--stable").text)
    apartment.append(link)
    apartments_features.append(apartment)

create_apartments_sql = '''create table if not exists apartments(
     apartment_id serial primary key,
     meterage int not null,
     created int not null,
     rooms int not null,
     total_price bigint not null,
     price_per_meter bigint not null,
     floor varchar(255) ,
     elevator varchar(255),
     parking varchar(255),
     warehouse varchar(255),
     link varchar(255)
     )'''
grant_sql = '''grant all on database apartment to postgres'''
insert_sql = '''insert into apartments
    (meterage,created,rooms,total_price,price_per_meter,floor,elevator,parking,warehouse,link)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''


def insert_in_database(cursor, create_table_sql, insert_sql):
    cursor.execute(create_table_sql)
    print("table created successfully........")
    for item in apartments_features:
        cursor.execute(insert_sql, item)


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

    cursor = conn.cursor()
    cursor.execute(grant_sql)
    insert_in_database(cursor, create_apartments_sql, insert_sql)
    cursor.close()
    conn.commit()
except (Exception, psycopg2.DatabaseError) as e:
    print(e)
finally:
    if conn is not None:
        conn.close()
