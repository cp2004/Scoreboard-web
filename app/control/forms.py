from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, ValidationError
from app.models import User
from flask import current_app

class NewGame_form(FlaskForm):
    player1 = SelectField('Player 1', validators=[DataRequired()], validate_choice=False)
    player2 = SelectField('Player 2', validators=[DataRequired()], validate_choice=False)
    serving = RadioField('First Server', validators=[DataRequired()], choices=[('p1', 'Player 1'),('p2', 'Player2')])
    submit = SubmitField('Submit')

    def validate_selection(self, player1, player2):
        if player1.data == player2.data:
            raise ValidationError('Please select two different players')
        