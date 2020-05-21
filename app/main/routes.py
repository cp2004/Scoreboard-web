from app import db
from app.main import bp
from flask import url_for, render_template, request
from flask_login import current_user, login_required, login_user, logout_user

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    try:
        return render_template('main/index.html', title="home")
    except:
        return "Game server unwell"