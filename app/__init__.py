from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cache import Cache
from config import config

db = SQLAlchemy()
mail = Mail()
cache = Cache()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_envvar("YOURAPPLICATION_SETTINGS")
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
