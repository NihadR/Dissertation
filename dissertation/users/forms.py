from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dissertation.models import User



class RegistrationForm(FlaskForm):
    '''
    Form for validating user input when signing up to the website 
    Uses different labels to which are passed through to the template
    '''
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        '''
        Checks whether the inputted username exists already
        '''
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken.')

    def validate_email(self, email):
        '''
        Checks whether the inputted email exists already
        '''
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken.')


class LoginForm(FlaskForm):
    '''
    Form for validating user input trying to login to the website
    Uses different labels to which are passed through to the template
    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccForm(FlaskForm):
    '''
    Form for validating user input when updating their account information
    Uses different labels to which are passed through to the template
    '''
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        '''
        Method for checking whether the username already exists in the 
        database
        '''
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken.')

    def validate_email(self, email):
        '''
        Method for checking whether the email already exists in the 
        database
        '''
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken.')


class RequestResetForm(FlaskForm):
    '''
    Form for checking the email given to change a password is valid
    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        '''
        Checks whether the email exists in the database 
        '''
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
    '''
    Validates the password when the user attempts to change their password
    '''
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
