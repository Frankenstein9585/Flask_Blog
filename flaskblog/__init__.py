from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
app = Flask(__name__)

app.config['SECRET_KEY'] = 'f657b43d1ee366f7cdc9912fd484f8d0'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqldb://flask:flaskpassword@localhost:3306/flask_db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
