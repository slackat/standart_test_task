from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse
from models import Requisites, PaymentRequests

invoices_bp = Blueprint('invoices', __name__, url_prefix='/api')
api = Api(invoices_bp)

class CreateInvoice(Resource):
    def get(self):
        payment_type = request.args.get('payment_type')
        limit = request.args.get('limit')
        
        if not (payment_type and limit):
            return {'message': 'Payment type and limit are required.'}, 400

        requisites = Requisites.query.filter(Requisites.payment_type == payment_type, Requisites.value_limit == limit).first()

        if requisites:
            return {'id': requisites.id,
                    'account_type': requisites.account_type,
                    'owner_name': requisites.owner_name,
                    'phone_number': requisites.phone_number
                    }, 200
        else:
            return {'message': 'Invoice not found'}, 404

class GetInvoiceStatus(Resource):
    def get(self, payment_id):
        if not payment_id:
            return {'message': 'ID is required.'}, 400
        
        payment = PaymentRequests.query.filter(PaymentRequests.id == payment_id).first()

        if payment:
            return {'invoice_status': payment.status}, 200
        else:
            return {'message': 'Invoice not found'}, 404


api.add_resource(GetInvoiceStatus, '/get_invoice_status/<int:payment_id>')
api.add_resource(CreateInvoice, '/create_invoice')
