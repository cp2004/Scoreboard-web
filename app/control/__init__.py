from flask import Blueprint

bp = Blueprint('control', __name__)

from app.control import routes