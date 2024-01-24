from flask import Blueprint, render_template, request
from sqlalchemy import or_
from models import PaymentRequests, Requisites
from utils import db

app_routes = Blueprint('app_routes', __name__)


@app_routes.route('/')
def payment_requests():
    requests = PaymentRequests.query.all()
    requisites = Requisites.query.all()

    data = {}

    for request in requests:
        data[request.id] = {
            'ID заявки': request.id,
            'Сумма': request.amount,
            'Статус': request.status,
        }

    for requisite in requisites:
        if requisite.id in data:
            data[requisite.id]['Тип оплаты'] = requisite.payment_type
            data[requisite.id]['Тип аккаунта'] = requisite.account_type
            data[requisite.id]['Имя'] = requisite.owner_name
            data[requisite.id]['Номер телефона'] = requisite.phone_number
            data[requisite.id]['Лимит'] = requisite.value_limit

    table_data = list(data.values())

    return render_template('payment_requests.html', data=table_data)


@app_routes.route('/requisites')
def requisites():
    column_to_sort = request.args.get('sort', 'id')
    order_by = request.args.get('order', 'asc')

    search_term = request.args.get('search', '')
    search_field = request.args.get('search_field', 'payment_type')

    field_mapping = {
        'payment_type': Requisites.payment_type,
        'account_type': Requisites.account_type,
        'owner_name': Requisites.owner_name,
        'phone_number': Requisites.phone_number,
        'limit': Requisites.value_limit,
    }

    if search_field not in field_mapping:
        return "Ничего не найдено"

    filters = [field_mapping[search_field].ilike(f'%{search_term}%')]
    requisites = Requisites.query.filter(or_(*filters)).order_by(db.text(f"{column_to_sort} {order_by}")).all()

    return render_template('requisites.html', requisites=requisites, column_to_sort=column_to_sort, order_by=order_by, search_term=search_term)

