"""
Project initialise file
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_swagger_ui import get_swaggerui_blueprint

"""
Configuring Flask app
"""
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'secret_key'
app.config['TESTING'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 60*60*24*30

"""
Configuring flask-swagger-ui
"""
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API Documentation"
    }
)

"""
Configuring database connection
"""
load_dotenv()
POSTGRES_LOGIN = os.getenv('POSTGRES_LOGIN')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_ADDRESS = os.getenv('POSTGRES_ADDRESS')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}/{POSTGRES_DATABASE}'
db = SQLAlchemy()
db.init_app(app)

"""
Configuring Bcrypt and LoginManager
"""
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app_routes.login'
