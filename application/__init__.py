from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
#from werkzeug.urls import url_encode

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from application import routes