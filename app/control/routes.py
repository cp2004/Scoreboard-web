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
    return render_template('control/game.html', title="Game in Progress")

@bp.route('/game/data/score', methods=['GET', 'POST'])
def backend():
    game = session.getSession()
    if request.method == 'GET':
        player1_score = game.getScore(game.player1)
        player2_score = game.getScore(game.player2)
        return "{} - {}".format(player1_score, player2_score)
    elif request.method == 'POST':
        data = request.json
        if data['command'] == 'p1':
            game.Score(game.player1)
        elif data['command'] == 'p2':
            game.Score(game.player2)
        player1_score = game.getScore(game.player1)
        player2_score = game.getScore(game.player2)
        return "{} - {}".format(player1_score, player2_score)