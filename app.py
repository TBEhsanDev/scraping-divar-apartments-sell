from flask import Flask, request, jsonify, render_template
from sqlalchemy.orm import Session

from models import Apartment, engine

app = Flask(__name__)


@app.route('/search', methods=['POST', 'GET'])
def search(*args, **kwargs):
    if request.method == 'POST':
        form = request.form
        l = []
        with Session(engine) as session:
            apartments = session.execute(session.query(Apartment)).scalars().all()
            for i in apartments:
                a = i.__dict__
                del a['_sa_instance_state']
                a[]
                l.append(a)
            return render_template('result.html', result=l)
    else:
        user = request.args.get('nm')
        return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
