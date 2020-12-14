import os
from os.path import join, dirname
from dotenv import load_dotenv
import pyodbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

login_manager = LoginManager()

path = join(dirname(__file__), '.env')
load_dotenv(path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# DATABASE CONFIGURATION
drivers = [d for d in pyodbc.drivers()]

SERVER = 'lexxserver.database.windows.net'
DATABASE = 'LexxSQL'
DRIVER = drivers[-1]
USERNAME = 'leo'
PASSWORD = os.getenv('DB_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# EMAIL CONFIGURATION
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

db = SQLAlchemy(app)
mail = Mail(app)

login_manager.init_app(app)
login_manager.login_view = 'login'

import project.views
