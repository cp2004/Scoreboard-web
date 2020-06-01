from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from config import Config

from app.game.session_manager import Session_Manager
from app.data.game_data import GameData
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
moment = Moment()

session = Session_Manager()
game_data = GameData()
if IS_RPI:
    matrix_obj = InitMatrix()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    game_data.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.control import bp as control_bp
    app.register_blueprint(control_bp)

    return app


from app import models
