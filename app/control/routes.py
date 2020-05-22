from app import db, session
from app.control import bp
from app.control.forms import NewGame_form
from app.game.game import Game as ttGame
from flask import url_for, render_template, request, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, Game

@bp.route('/game/new', methods=['GET', 'POST'])
@login_required
def new_game():
    form = NewGame_form()
    users = User.query.all()
    form.player1.choices = [(user.id, user.username) for user in users]
    form.player2.choices = [(user.id, user.username) for user in users]
    if form.validate_on_submit():
        if not session.is_active():
            game = ttGame(form.player1.data, form.player2.data) #Need to define first serve...
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
    game = session.getSession()
    player1 = User.query.filter_by(id=game.player1.user).first_or_404().username
    player2 = User.query.filter_by(id=game.player2.user).first_or_404().username
    players = {'player1':player1, 'player2':player2}
    return render_template('control/game.html', title="Game in Progress", players=players)

@bp.route('/game/data/scoreboard', methods=['GET', 'POST'])
def scoreboard():
    game = session.getSession()
    if request.method == 'POST':
        data = request.json
        if data['command'] == 'p1':
            game.Score(game.player1)
        elif data['command'] == 'p2':
            game.Score(game.player2)
        elif data['command'] == 'subp1':
            game.subtract(game.player1)
        elif data['command'] == 'subp2':
            game.subtract(game.player2)

    if game.getWinner():
        winner = WinnerData()
        winner.name = User.query.filter_by(id=game.getWinner().user).first_or_404().username
        winner.score = game.getScore(game.winner)
        if game.getWinner() == game.player1:
            winner.against = User.query.filter_by(id=game.player2.user).first_or_404().username
            winner.against_score = game.getScore(game.player2)
        else:
            winner.against = User.query.filter_by(id=game.player1.user).first_or_404().username
            winner.against_score = game.getScore(game.player1)
        return render_template('control/win.html', title="Game Won", winner=winner)
    
    else:
        data = ScoreboardData()
        data.player1_score = game.getScore(game.player1)
        data.player2_score = game.getScore(game.player2)
        data.serving = game.getServe()
        return render_template('control/scoreboard.html', data=data)

class ScoreboardData():
    player1_score = 0
    player2_score = 0
    serving = 0

class WinnerData():
    name = None
    against = None
    score = None
    against_score = None

@bp.route('/game/save')
def save_game():
    game = session.getSession
    savegame = Game(player1=game.player1.user,
                    player2=game.player2.user,
                    player1_score=game.getScore(game.player1),
                    player2_score=game.getScore(game.player2),
                    winner=game.getWinner().user)
    db.session.add(savegame)
    db.session.commit()
    session.endSession()
    flash('Game saved', category='success')
    return redirect(url_for('main.index'))

@bp.route('/game/discard')
def discard_game():
    session.endSession()
    return redirect(url_for('main.index'))