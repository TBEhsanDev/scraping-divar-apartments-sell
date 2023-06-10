from flask import Flask, request, render_template
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Apartment, engine

app = Flask(__name__)


@app.route('/search', methods=['POST', 'GET'])
def search(*args, **kwargs):
    if request.method == 'POST':
        form = {key: val for key, val in request.form.items() if val}
        meterage = form.get('meterage')
        made_date = form.get('made_date')
        rooms = form.get('rooms')
        min_total_price = form.get('min_total_price')
        max_total_price = form.get('max_total_price')
        min_price_per_meter = form.get('min_price_per_meter')
        l = []
        with Session(engine) as session:
            apartments = session.scalars(Apartment.select().where(
                getattr(Apartment,'') >= int(meterage),
                Apartment.made_date >= int(made_date),
                Apartment.rooms >= int(rooms),
                Apartment.total_price >= int(min_total_price) * 1_000_000,
                Apartment.total_price <= int(max_total_price) * 1_000_000,
                Apartment.price_per_meter >= int(min_price_per_meter)
            )).all()
        for i, item in enumerate(apartments):
            a = item.__dict__
            del a['_sa_instance_state']
            a['count'] = i
            l.append(a)
        return render_template('result.html', result=l)
    else:
        user = request.args.get('nm')
        return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
