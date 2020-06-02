from app import db, session, game_data
from app.main import bp
from flask import url_for, render_template, request, redirect, flash
from flask_login import current_user, login_required
from app.models import User
from app.main.forms import EditProfileForm


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    if session.is_active():
        currentSession = session.getSessionId()
    else:
        currentSession = None
    games = game_data.getIndex()

    return render_template('main/index.html', user=current_user, title="Home", reversed=reversed, currentSession=currentSession, games=games, game_data=game_data, User=User)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    games = game_data.loadUser(user.id)['games']

    return render_template('main/user.html', user=user, reversed=reversed, title=user.username, games=games, game_data=game_data, User=User)


@bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.initial = form.initial.data
        db.session.commit()
        flash('Your changes have been saved.', category='success')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.initial.data = current_user.initial

    games = game_data.getIndex()
    return render_template('main/edit_profile.html', title='Edit Profile', form=form, user=user, games=games, game_data=game_data, User=User)


@bp.route('/delete/<id>')
@login_required
def delete_game(id):
    game = game_data.loadGame(id)
    if current_user.id == int(game['player1']['id']) or current_user.id == int(game['player2']['id']):
        game_data.deletegame(id)
    # Redirect to previous page?
    return redirect(url_for('main.index'))


@bp.route('/list')
@login_required
def feature_list():
    return render_template('main/feature_list.html')
