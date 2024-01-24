"""
Project initialise file
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

load_dotenv()
POSTGRES_LOGIN = os.getenv('POSTGRES_LOGIN')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_ADDRESS = os.getenv('POSTGRES_ADDRESS')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}/{POSTGRES_DATABASE}'
db = SQLAlchemy()
db.init_app(app)
