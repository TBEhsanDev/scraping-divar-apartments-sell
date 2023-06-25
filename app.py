import jwt
from flask import request, render_template, send_file, make_response
from sqlalchemy.orm import Session

from models import Apartment, engine, User
from scrape import scrape
from settings import app
from utils import token_required, create_excel


@app.route('/download', methods=['GET'])
def excel():
    path = './apartments_divar.xlsx'
    with Session(engine) as session:
        apartments = session.scalars(Apartment.select(), execution_options={"stream_results": True}).all()
    result = Apartment.query_result_to_list_of_dict(apartments)
    create_excel.delay(result)
    return send_file(path_or_file=path, download_name='apartments_divar.xlsx', as_attachment=True)


@app.route('/search', methods=['POST', 'GET'])
@token_required
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

        with Session(engine) as session:
            apartments = Apartment.select_from_database(Apartment.made_date >= int(made_date) if made_date else True,
                                                        Apartment.rooms >= int(rooms) if rooms else True,
                                                        Apartment.total_price >= int(
                                                            min_total_price) * 1_000_000 if min_total_price else True,
                                                        Apartment.total_price <= int(
                                                            max_total_price) * 1_000_000 if max_total_price else True,
                                                        Apartment.price_per_meter >= int(
                                                            min_price_per_meter) if min_price_per_meter else True)

        result = Apartment.query_result_to_list_of_dict(apartments)
        return render_template('result.html', result=result)
    # else:
    #     return render_template('search.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'username': request.form.get('username'),
            'password': request.form.get('password'),
        }
        User.insert_in_database(user)
        return render_template('login.html')
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user: User = User.select_from_database(User.username == username, User.password == password)[0]
        if user:
            token = jwt.encode({'username': user.username}, app.config['SECRET_KEY'], algorithm="HS256")
            resp = make_response(render_template('search.html', message=f'{user.first_name} {user.last_name}'))
            resp.set_cookie('jwt', token)
            return resp
        else:
            return render_template('login.html', message='wrong username or password')
    else:
        return render_template('login.html', message='Enter username and password')


@app.route('/logout', methods=['GET'])
def logout():
    token = request.cookies.get('jwt')
    if token:
        resp = make_response(render_template('login.html', message='Enter username and password'))
        resp.set_cookie('jwt', '', expires=0)
        return resp


if __name__ == '__main__':
    app.run(debug=True)
