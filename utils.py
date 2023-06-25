import jwt
import xlsxwriter
from flask import request, render_template

from models import User
from settings import app, celery


def token_required(f):
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt')
        if token:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            user: User = User.select_from_database(User.username == data['username'])
            if user:
                return f(*args, **kwargs)
            else:
                return render_template('login.html', message='Enter username and password')

    return decorated


@celery.task(name='create_excel', bind=True)
def create_excel(self, result):
    workbook = xlsxwriter.Workbook('apartments_divar.xlsx')
    worksheet = workbook.add_worksheet()

    headers = {'count': 10, 'meterage': 15, 'made_date': 15, 'rooms': 15,
               'size_of_land': 15, 'floors': 15, 'features': 20, 'price_per_meter': 15,
               'description': 50, 'total_price': 15, 'advertiser': 15, 'link': 30}

    for row_num, data in enumerate(result):
        if row_num == 0:
            [(worksheet.write(0, i, key), worksheet.set_column(i, i, headers[key])) for i, key in
             enumerate(list(data.keys()))]
        for cul_num, value in enumerate(data.values()):
            if isinstance(value, list):
                value = ''.join(value)
            worksheet.write(row_num + 1, cul_num, value)

    workbook.close()
