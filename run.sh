#!/bin/bash -x
python3 ./create_db.py
python3 ./scrape.py
python3 ./app.py