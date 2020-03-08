from flask import Flask, escape, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'ecef3b8e7d47ea8a26b098bc534393dd'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ss117_hard_disk_guru_web:DatabasePassword@localhost/ss117_harddrive'
#db = SQLAlchemy(app)



# # coding: utf-8
# from sqlalchemy import Column, Date, ForeignKey, Index, String, Table
# from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
# metadata = Base.metadata


# class DiskManufacturer(Base):
#     __tablename__ = 'DiskManufacturer'

#     ManufacturerID = Column(VARCHAR(32), primary_key=True)
#     ManufacturerName = Column(VARCHAR(255), nullable=False)


# class User(Base):
#     __tablename__ = 'User'

#     UserID = Column(INTEGER(11), primary_key=True)
#     Email = Column(String(256), nullable=False)
#     Password = Column(String(32), nullable=False, comment='MD5 hash')


# class DiskModel(Base):
#     __tablename__ = 'DiskModel'

#     DiskModelID = Column(VARCHAR(35), primary_key=True)
#     ManufacturerID = Column(ForeignKey('DiskManufacturer.ManufacturerID'), index=True)
#     CapacityBytes = Column(BIGINT(14))

#     DiskManufacturer = relationship('DiskManufacturer')


# t_DiskDailyLog = Table(
#     'DiskDailyLog', metadata,
#     Column('date', Date, nullable=False),
#     Column('serial_number', String(32), nullable=False),
#     Column('model', ForeignKey('DiskModel.DiskModelID'), index=True),
#     Column('capacity_bytes', BIGINT(14)),
#     Column('failure', INTEGER(1)),
#     Index('UK_Date_Serial', 'date', 'serial_number', unique=True)
# )


# t_UserDisk = Table(
#     'UserDisk', metadata,
#     Column('UserID', ForeignKey('User.UserID'), nullable=False),
#     Column('DiskModellD', ForeignKey('DiskModel.DiskModelID'), index=True),
#     Column('SerialNumber', String(32), nullable=False),
#     Column('ManufactureDate', Date),
#     Index('UK_User_SerialNum', 'UserID', 'SerialNumber', unique=True)
# )



@app.route('/')
@app.route('/home')
def home():
    #name = request.args.get("name", "Page")
    return render_template('home.html', title = 'Home')

@app.route('/about')
def about():
    #name = request.args.get("name", "Page")
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


if __name__ == '__main__':
    app.run(debug=True)