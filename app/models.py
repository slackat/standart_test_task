from utils import db

class Requisites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(db.String(100))
    account_type = db.Column(db.String(100))
    owner_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    value_limit = db.Column(db.Integer)

class PaymentRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    status = db.Column(db.String(100))
