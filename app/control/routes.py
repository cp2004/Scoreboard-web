from app import db, session
from app.control import bp
from app.control.forms import NewGame_form
from app.game.game import Game
from flask import url_for, render_template, request, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User

@bp.route('/game/new', methods=['GET', 'POST'])
@login_required
def new_game():
    form = NewGame_form()
    users = User.query.all()
    form.player1.choices = [(user.id, user.username) for user in users]
    form.player2.choices = [(user.id, user.username) for user in users]
    if form.validate_on_submit():
        if not session.is_active():
            game = Game(form.player1.data, form.player2.data) #Need to define first serve...
            session.setSession(game)
            return redirect(url_for('control.game', gameid=session.getSessionId()))
        else:
            flash('Game session already created', category='error')
    return render_template('/control/newgame.html', title="New Game", form=form)

@bp.route('/game/<gameid>')
@login_required
def game(gameid):
    currentId = session.getSessionId()
    if int(gameid) != currentId:
        return redirect(url_for('main.index'))
    return "Game in progress: {}".format(gameid)

@bp.route('/game/backend/<sessionid>')
def backend(sessionid):
    return "Backend not functioning...."