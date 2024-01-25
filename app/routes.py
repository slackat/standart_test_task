from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import or_
from models import PaymentRequests, Requisites
from utils import db

app_routes = Blueprint('app_routes', __name__)


@app_routes.route("/")
def payment_requests():
    joined_data = db.session.query(PaymentRequests, Requisites).outerjoin(Requisites,
                                                                     PaymentRequests.id == Requisites.id
                                                                     ).all()

    data = {}

    for payment_request, requisite in joined_data:
        data[payment_request.id] = {
            'ID заявки': payment_request.id,
            'Сумма': payment_request.amount,
            'Статус': payment_request.status,
            'Тип оплаты': requisite.payment_type if requisite else '',
            'Тип аккаунта': requisite.account_type if requisite else '',
            'Имя': requisite.owner_name if requisite else '',
            'Номер телефона': requisite.phone_number if requisite else '',
            'Лимит': requisite.value_limit if requisite else ''
        }

    table_data = list(data.values())

    return render_template('payment_requests.html', data=table_data)


@app_routes.route('/requisites')
def requisites():
    requisites = Requisites.query.all()
    return render_template('requisites.html', requisites=requisites)


@app_routes.route('/get_requisites')
def get_requisites():
    column_to_sort = request.args.get('sort', 'id')
    order_by = request.args.get('order', 'asc')
    search_term = request.args.get('search', '')
    search_field = request.args.get('search_field', 'payment_type')

    field_mapping = {
        'payment_type': Requisites.payment_type,
        'account_type': Requisites.account_type,
        'owner_name': Requisites.owner_name,
        'phone_number': Requisites.phone_number,
        'value_limit': Requisites.value_limit,
    }

    if search_field not in field_mapping:
        return jsonify([])

    filters = [field_mapping[search_field].ilike(f'%{search_term}%')]
    requisites = Requisites.query.filter(
        or_(*filters)).order_by(db.text(f"{column_to_sort} {order_by}")).all()

    requisites_data = [{'id': req.id, 'payment_type': req.payment_type, 'account_type': req.account_type,
                        'owner_name': req.owner_name, 'phone_number': req.phone_number, 'value_limit': req.value_limit}
                       for req in requisites]

    print(requisites_data)
    return jsonify(requisites_data)
