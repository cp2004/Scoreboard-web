from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, ValidationError


class NewGame_form(FlaskForm):
    player1 = SelectField('Player 1', validators=[DataRequired("Please select a player")], coerce=int, validate_choice=True)
    player2 = SelectField('Player 2', validators=[DataRequired("Please select a player")], coerce=int, validate_choice=True)
    serving = RadioField('First Server', validators=[DataRequired("Please select a player to serve")], choices=[('p1', 'Player 1'), ('p2', 'Player2')])
    submit = SubmitField('Start Game')

    def validate_player1(self, player1):
        if player1.data == self.player2.data:
            raise ValidationError('Please select two different players')

    def validate_player2(self, player2):
        if player2.data == self.player1.data:
            raise ValidationError('Please select two different players')
