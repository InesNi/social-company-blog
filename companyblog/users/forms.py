from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                Regexp, ValidationError)
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from companyblog.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators =[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField(
        'Password', validators =[DataRequired(),
        EqualTo('pass_confirm', message='Passwords must match'),
        Length(min=8)]
        )
    pass_confirm = PasswordField(
        'Confirm password', validators =[DataRequired()]
        )
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_usename(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'Your username has been registered already!'
                )


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg','png', 'jpeg'])]
        )
    submit = SubmitField('Update')

    def __init__(self, orig_username, orig_email, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.orig_username = orig_username
        self.orig_email = orig_email

    def validate_email(self, orig_email):
        if self.email.data != self.orig_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                raise ValidationError(
                    'Your email has been registered already!'
                )

    def validate_usename(self, orig_username):
        if self.username.data != self.orig_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                raise ValidationError(
                    'Your username has been registered already!'
                )
