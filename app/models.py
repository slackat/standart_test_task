from utils import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    user_role = db.Column(db.Enum('admin', 'user', name='user_role'), nullable=False)


class Requisites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(db.String(100))
    account_type = db.Column(db.String(100))
    owner_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    value_limit = db.Column(db.Integer)
    payment_requests = db.relationship('PaymentRequests', backref=backref('requisites', cascade="all,delete"), lazy=True)


class PaymentRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    status = db.Column(db.String(100))
    requisites_id = db.Column(db.Integer, ForeignKey('requisites.id'), nullable=True)