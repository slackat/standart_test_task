"""
File for database seeding
"""

from faker import Faker
import random
from models import Requisites, PaymentRequests, User
from . import app, db, bcrypt, ADMIN_PASSWORD_FOR_REQUISITES

fake = Faker()

PAYMENT_WITH_REQUISITES = random.sample(range(1, 5001), 100)
PAYMENT_ID_WITH_AMOUNT = {payment_id:random.randint(100, 10000) for payment_id in PAYMENT_WITH_REQUISITES}

def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Seeding requisites table
        for payment_id in PAYMENT_WITH_REQUISITES:
            requisites = Requisites(
                id = payment_id,
                payment_type=random.choice(['card', 'bank_account']),
                account_type=random.choice(['visa', 'mastercard', 'savings', 'checking']),
                owner_name=fake.name(),
                phone_number=fake.phone_number(),
                value_limit=PAYMENT_ID_WITH_AMOUNT[payment_id],
            )
            db.session.add(requisites)

        db.session.commit()

        # Seeding requests table
        for payment_id in range(1, 5000):
            if payment_id in PAYMENT_WITH_REQUISITES:
                request = PaymentRequests(
                    id=payment_id,
                    amount=PAYMENT_ID_WITH_AMOUNT[payment_id],
                    status='paid',
                )
            else:
                request = PaymentRequests(
                    id=payment_id,
                    amount=random.randint(0, 10000),
                    status=random.choice(['waiting_payment', 'canceled']),
                )
            db.session.add(request)
        
        db.session.commit()

        # Seeding user table
        admin = User(
            username = 'admin',
            password = bcrypt.generate_password_hash(ADMIN_PASSWORD_FOR_REQUISITES).decode('utf-8'),
            user_role = 'admin'
        )
        db.session.add(admin)

        db.session.commit()
