import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


from config import Config
from app.game.session_manager import Session_Manager
from app.data import GameData
try:
    from app.matrix.graphics import InitMatrix
    IS_RPI = True
    print("Matrix graphics supported")
except ImportError or ModuleNotFoundError:
    IS_RPI = False
    print("Matrix graphics not supported")

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page'

session = Session_Manager()
game_data = GameData()
if IS_RPI:
    matrix_obj = InitMatrix()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.testing and not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/tabletennis.log.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)  # Configure from app?
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("App startup begun")

    game_data.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.control import bp as control_bp
    app.register_blueprint(control_bp)

    app.logger.info('Table Tennis app startup Complete')
    return app


from app import models
