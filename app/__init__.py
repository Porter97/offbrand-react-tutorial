from flask import Flask
from .extensions import db, login_manager
from config import config


def create_app(config_name):
    app = Flask(__name__, static_folder='./static/dist', template_folder='./static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app