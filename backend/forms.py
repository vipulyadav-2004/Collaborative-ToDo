from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired ,Length,Email,EqualTo
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import ValidationError  # <-- 1. Import ValidationError
from .models import User

class RegistrationForms(FlaskForm):
    username = StringField('Username' , validators=[DataRequired() , Length(min=2,max=20)])
    email = StringField('Email' , validators=[DataRequired()  , Email()])
    password = PasswordField('Password' ,  validators=[DataRequired(), Length(min=8)])
    confirm_password  = PasswordField('ConfirmPassword' , validators=[DataRequired() , EqualTo('password')])
    signup = SubmitField('Signup')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another.')

    # 4. Add this custom validation method for email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose another.')


class LoginForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired() , Length(min=2,max=20)])
   
    password = PasswordField('Password' ,  validators=[DataRequired()])
    remember = BooleanField('Remember me !')
    signup = SubmitField('Login')

class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Delete')