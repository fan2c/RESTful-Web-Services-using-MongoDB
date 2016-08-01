from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import config

mail = Mail()
moment = Moment()
mongo = PyMongo()

login_manager = LoginManager()
login_manager.session_protection = 'strong'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
