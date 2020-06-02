from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Email
from wtforms.fields.html5 import EmailField
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Username is required")])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140, message="Max 140 characters")])
    submit = SubmitField('Save')
    initial = StringField('Initial', validators=[DataRequired("Initials required"), Length(2, 2, message="Initials shoud be 2 characters")])
    email = EmailField('Email', validators=[Email("Please use a valid email address")])

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username already taken')
        if ' ' in username.data:
            raise ValidationError('No spaces in username please')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
