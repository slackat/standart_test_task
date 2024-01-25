from flask import Blueprint, jsonify, render_template, request, send_file, url_for, redirect
from sqlalchemy import or_
from models import PaymentRequests, Requisites, User
from utils import db, login_manager, bcrypt
from flask_login import login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

app_routes = Blueprint('app_routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Логин"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Пароль"})

    submit = SubmitField('Войти')

@app_routes.route('/')
def home():
    return render_template('home.html')


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('app_routes.payment_requests'))
    return render_template('login.html', form=form)


@app_routes.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('app_routes.home'))


@app_routes.route("/payment_requests")
def payment_requests():
    joined_data = db.session.query(PaymentRequests, Requisites).outerjoin(Requisites,
                                                                     PaymentRequests.id == Requisites.id
                                                                     ).all()

    table_data = [{'id': payment_request.id,
                   'amount': payment_request.amount,
                   'status': payment_request.status,
                   'payment_type': getattr(requisite, 'payment_type', ''),
                   'account_type': getattr(requisite, 'account_type', ''),
                   'owner_name': getattr(requisite, 'owner_name', ''),
                   'phone_number': getattr(requisite, 'phone_number', ''),
                   'value_limit': getattr(requisite, 'value_limit', '')
                   }
                   for payment_request, requisite in joined_data]

    return render_template('payment_requests.html', data=table_data)


@app_routes.route('/requisites')
@login_required
def requisites():
    requisites = Requisites.query.all()
    return render_template('requisites.html', requisites=requisites)


@app_routes.route('/get_requisites')
@login_required
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

    if search_term:
        # For integer columns
        if search_field == 'value_limit':
            try:
                search_term = int(search_term)
            except ValueError:
                return jsonify([])
            filters = [field_mapping[search_field] == search_term]
        # For string columns
        else:
            filters = [field_mapping[search_field].ilike(f'%{search_term}%')]

        requisites = Requisites.query.filter(
            or_(*filters)).order_by(db.text(f"{column_to_sort} {order_by}")).all()
    else:
        # In case empty search field for show all data
        requisites = Requisites.query.order_by(db.text(f"{column_to_sort} {order_by}")).all()

    requisites_data = [{'id': req.id, 'payment_type': req.payment_type, 'account_type': req.account_type,
                        'owner_name': req.owner_name, 'phone_number': req.phone_number, 'value_limit': req.value_limit}
                       for req in requisites]

    return jsonify(requisites_data)

@app_routes.route('/static/swagger.json')
def get_swagger_json():
    swagger_file_path = '../swagger/swagger.json'
    return send_file(swagger_file_path)
