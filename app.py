from flask import Flask, request, render_template
from sqlalchemy.orm import Session

from models import Apartment, engine
from scrape import scrape

app = Flask(__name__)


@app.route('/search', methods=['POST', 'GET'])
def search(*args, **kwargs):
    if request.method == 'POST':
        form = {key: val for key, val in request.form.items() if val}
        update = form.get('update')
        meterage = form.get('meterage')
        made_date = form.get('made_date')
        rooms = form.get('rooms')
        min_total_price = form.get('min_total_price')
        max_total_price = form.get('max_total_price')
        min_price_per_meter = form.get('min_price_per_meter')
        if update:
            scrape(update=True)
        l = []
        with Session(engine) as session:
            apartments = session.scalars(Apartment.select().where(
                Apartment.meterage >= int(meterage) if meterage else True,
                Apartment.made_date >= int(made_date) if made_date else True,
                Apartment.rooms >= int(rooms) if rooms else True,
                Apartment.total_price >= int(min_total_price) * 1_000_000 if min_total_price else True,
                Apartment.total_price <= int(max_total_price) * 1_000_000 if max_total_price else True,
                Apartment.price_per_meter >= int(min_price_per_meter) if min_price_per_meter else True
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
