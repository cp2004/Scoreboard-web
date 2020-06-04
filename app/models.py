from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    initial = db.Column(db.String(2))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)  # Could move to stats - Currently unused
    stats = db.relationship("Stats", uselist=False, back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        if self.email:
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        else:
            return '/static/no_email.svg'


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="stats")

    games_played = db.Column(db.Integer)
    games_won = db.Column(db.Integer)
    total_points = db.Column(db.Integer)
    total_points_against = db.Column(db.Integer)
    avg_points = db.Column(db.Integer)
    avg_points_against = db.Column(db.Integer)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
