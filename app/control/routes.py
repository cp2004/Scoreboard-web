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
            if form.serving.data == 'p1':
                game.setServe(game.player1)
            else:
                game.setServe(game.player2)
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

@bp.route('/game/data/scoreboard', methods=['GET', 'POST'])
def scoreboard():
    game = session.getSession()
    if request.method == 'POST':
        data = request.json
        if data['command'] == 'p1':
            game.Score(game.player1)
        elif data['command'] == 'p2':
            game.Score(game.player2)
    data = ScoreboardData()
    data.player1_score = game.getScore(game.player1)
    data.player2_score = game.getScore(game.player2)
    data.serving = game.getServe()
    return render_template('control/scoreboard.html', data=data)

class ScoreboardData():
    player1_score = 0
    player2_score = 0
    serving = 0