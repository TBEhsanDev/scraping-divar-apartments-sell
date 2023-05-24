from functools import wraps

from flask import Flask, redirect, url_for, request, json, jsonify
from sqlalchemy.orm import Session

from models import Apartment, engine, Base

app = Flask(__name__)


@app.route('/success/<name>')
def success(name):
    return ''


@app.route('/search', methods=['POST', 'GET'])
def search(*args, **kwargs):
    if request.method == 'POST':
        l = []
        with Session(engine) as session:
            apartments = session.execute(session.query(Apartment)).scalars().all()
            for i in apartments:
                a=i.__dict__
                del a['_sa_instance_state']
                l.append(a)
            m=jsonify(l)
            return  m
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


if __name__ == '__main__':
    app.run(debug=True)
