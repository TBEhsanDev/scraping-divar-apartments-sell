from celery import Celery
from flask import Flask

app = Flask('app')
app.config['SECRET_KEY'] = 'ehsan'
celery = Celery(
    'app',
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

