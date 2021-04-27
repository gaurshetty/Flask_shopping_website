from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from flask_login import current_user
from shopping_website.market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=3, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    remember = BooleanField(label='Remember me!')
    submit = SubmitField(label='Sign In')


class AccountForm(FlaskForm):
    def validate_username(self, username_to_check):
        if username_to_check.data != current_user.username:
            user = User.query.filter_by(username=username_to_check.data).first()
            if user:
                raise ValidationError('Username already exists! Please try a different username')

    def validate_email(self, email_to_check):
        if email_to_check.data != current_user.email:
            email = User.query.filter_by(email=email_to_check.data).first()
            if email:
                raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    image_file = FileField(label='Update profile picture:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Update')


class RequestResetForm(FlaskForm):
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with given email! You must register first.')


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Reset Password')
