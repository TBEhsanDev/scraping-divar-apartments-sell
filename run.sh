#!/bin/bash -x
python3 ./create_db.py
python3 ./scrape.py
celery -A app.celery worker  --pool=solo --loglevel=info &
python3 ./app.py