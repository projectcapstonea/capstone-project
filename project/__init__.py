import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()

path = join(dirname(__file__), '.env')
load_dotenv(path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

SERVER = 'tcp:ifood-server.database.windows.net'
DATABASE = 'iFood'
DRIVER = 'ODBC Driver 17 for SQL Server'
USERNAME = 'dbadmin'
PASSWORD = os.getenv('DB_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = 'DRIVER={'+DRIVER+'};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+PASSWORD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager.init_app(app)
login_manager.login_view = 'login'

import project.views
