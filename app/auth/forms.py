from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Please enter a username")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Please enter a username")])
    initial = StringField('Initial', validators=[DataRequired("Please enter initials"), Length(min=2, max=2, message="Initials should be 2 characters")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
    password2 = PasswordField('Repeat Password', validators=[DataRequired("Please repeat your password"), EqualTo('password', message="Passwords should be equal")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            current_app.logger.info(f"Request for username {user.username} denied, already taken")
            raise ValidationError('Username already taken')
        if ' ' in username.data:
            current_app.logger.info(f'Request for username {user.username} denied, spaces in name')
            raise ValidationError('No spaces in username please')
