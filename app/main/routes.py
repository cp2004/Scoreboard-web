from app import db, session, game_data
from app.main import bp
from flask import url_for, render_template, request, redirect
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    if session.is_active():
        currentSession = session.getSessionId()
    else:
        currentSession = None
    games = game_data.getIndex()

    return render_template('main/index.html', title="Home", reversed=reversed, currentSession=currentSession, games=games, game_data=game_data, User=User )


@bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    games = game_data.loadUser(user.id)['games']

    return render_template('main/user.html', user=user, reversed=reversed, title=user.username, games=games, game_data=game_data, User=User)

@bp.route('/delete/<id>')
def delete_game(id):
    game_data.deletegame(id)
    #Redirect to previous page?
    return redirect(url_for('main.index'))