from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from HardDiskGuru.models import User
from HardDiskGuru import db

class RegistrationForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = db.session.query(User).filter(User.email == email.data).first()
        if user:
            raise ValidationError('That email is already associated with an account. Register with a different email or log in.')

class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# class QueryManufacturerHardDisksForm(FlaskForm):
#     manufacturer_name = StringField('Manufacturer Name',
#         validators=[DataRequired()])
#     submit = SubmitField('Query')