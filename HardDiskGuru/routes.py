from flask import escape, request, render_template, url_for, flash, redirect
from HardDiskGuru import app, db, bcrypt
from HardDiskGuru.forms import RegistrationForm, LoginForm, EnterDiskModelForm
from HardDiskGuru.models import DiskManufacturer, DiskModel, User, UserDisk
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    #form = QueryManufacturerHardDisksForm()
    #result_set = []
    # if form.manufacturer_name.data != None:
    #     results = db.session.query(DiskModel).filter(DiskModel.ManufacturerID == form.manufacturer_name.data).limit(3)
    #     for r in results:
    #         result_set.append([r.DiskModelID,r.ManufacturerID,r.CapacityBytes])
    return render_template('home.html', title = 'Home') #, form = form, result_set = result_set)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = 'Account')

@app.route("/enterharddisks", methods = ['GET', 'POST'])
@login_required
def enter_hard_disks():
    form = EnterDiskModelForm()
    if form.validate_on_submit():
        userdisk = UserDisk(userid=current_user.id,
            diskmodelid=form.disk_model.data,
            serialnumber=form.serial_number.data,
            manufacturedate=form.manufacture_date.data)
        db.session.add(userdisk)
        db.session.commit()
        flash('Your hard disk has been added.', 'success')
    return render_template('enter_hard_disks.html', title = 'Enter Hard Disks', form = form)

@app.route("/myharddisks", methods = ['GET', 'POST'])
@login_required
def my_hard_disks():
    my_user_disks = db.session.query(UserDisk).filter(UserDisk.userid == current_user.id).all()
    return render_template('my_hard_disks.html', title = 'My Hard Disks', my_user_disks = my_user_disks)