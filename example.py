# example.py
import time

from celery import Celery
from flask import Flask

app = Flask('example')
# app.config['CELERY_BROKER_URL'] = 'redis://localhost'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost'
# celery = Celery(app)

celery = Celery(
    'example',
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)


@app.route("/")
def hello():
    return "Hello, World!"


@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y
@celery.task()
def add_together(a, b):
    time.sleep(3)
    return a + b


if __name__ == '__main__':
    result = add_together.delay(23, 42)
    print()
