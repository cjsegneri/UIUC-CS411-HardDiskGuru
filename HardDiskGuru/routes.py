from flask import escape, request, render_template, url_for, flash, redirect
from HardDiskGuru import app
from HardDiskGuru.forms import RegistrationForm, LoginForm, QueryManufacturerHardDisksForm
from HardDiskGuru.models import DiskManufacturer, DiskModel, User
from HardDiskGuru import db


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = QueryManufacturerHardDisksForm()
    result_set = []
    #if form.manufacturer_name.data != None:
        #results = db.session.query(DiskModel).filter(DiskModel.ManufacturerID == form.manufacturer_name.data).limit(3)
        #for r in results:
            #result_set.append([r.DiskModelID,r.ManufacturerID,r.CapacityBytes])
    return render_template('home.html', title = 'Home', form = form, result_set = result_set)

@app.route('/about')
def about():
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
