from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from HardDiskGuru.models import User, DiskManufacturer, DiskModel, UserDisk
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

class EnterDiskModelForm(FlaskForm):
    # manufacturer_choices = db.session.query(DiskManufacturer).all()
    # manufacturer = SelectField('Manufacturer',
    #     validators=[DataRequired()],
    #     choices = [(m.manufacturerid,m.manufacturerid) for m in manufacturer_choices])
    
    disk_model_choices = db.session.query(DiskModel).all()
    disk_model = SelectField('Disk Model',
        validators=[DataRequired()],
        choices = [(d.diskmodelid,d.diskmodelid) for d in disk_model_choices])
    
    serial_number = StringField('Serial Number',
        validators=[DataRequired()])
    
    manufacture_date = DateField('Manufacture Date',
        validators=[DataRequired()], format='%Y-%m-%d')
    
    submit = SubmitField('Submit')

    def validate_serial_number(self, serial_number):
        userdisk = db.session.query(UserDisk).filter(UserDisk.serialnumber == serial_number.data).first()
        if userdisk:
            raise ValidationError('You have already entered a hard disk with that serial number.')