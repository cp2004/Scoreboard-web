from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.Integer) #ID of player 1
    player2 = db.Column(db.Integer) #ID of player 2
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    player1_score = db.Column(db.Integer) #P1 Score
    player2_score = db.Column(db.Integer) #P2 Score
    winner = db.Column(db.Integer) #ID of winner (Could be done from scores but this is quicker)

    def __repr__(self):
        return '<Game between {} and {} scored {}-{} at {}>'.format(self.player1, self.player2, self.player1_score, self.player2_score, self.timestamp)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))