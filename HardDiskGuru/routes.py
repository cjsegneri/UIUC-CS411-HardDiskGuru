from flask import escape, request, render_template, url_for, flash, redirect
from sqlalchemy import text
import json
from HardDiskGuru import app, db, bcrypt
from HardDiskGuru.forms import RegistrationForm, LoginForm, EnterDiskModelForm
from HardDiskGuru.models import DiskManufacturer, DiskModel, User, UserDisk
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    results = db.engine.execute(text("""
        (SELECT
            DiskModelID,
            ReliabilityScore
        FROM ss117_harddrive.diskmodel
        WHERE ReliabilityScore IS NOT NULL
        ORDER BY ReliabilityScore DESC
        LIMIT 5)
        UNION
        (SELECT
            DiskModelID,
            ReliabilityScore
        FROM ss117_harddrive.diskmodel
        WHERE ReliabilityScore IS NOT NULL
        ORDER BY ReliabilityScore ASC
        LIMIT 5);
    """))
    results = [row for row in results]
    manufacturer_counts = db.engine.execute(text("""
        SELECT
            DMR.ManufacturerID,
            SUM(DDS.TotalDiskCount) AS NumberOfTests,
            SUM(DDS.TotalDiskCount) - SUM(DDS.FailureCount) AS FailureCount
        FROM ss117_harddrive.diskmanufacturer DMR
            JOIN ss117_harddrive.diskmodel DML ON DML.ManufacturerID = DMR.ManufacturerID
            JOIN ss117_harddrive.diskdailystats DDS ON DDS.DiskModelID = DML.DiskModelID
        GROUP BY DMR.ManufacturerID;
    """))
    manufacturer_counts = [row for row in manufacturer_counts]
    return render_template('home.html', title = 'Home', results = results, manufacturer_counts = manufacturer_counts) #, form = form, result_set = result_set)

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
    return render_template('enter_hard_disks.html', title = 'Enter Hard Disk', form = form)

@app.route("/myharddisks", methods = ['GET', 'POST'])
@login_required
def my_hard_disks():
    #my_user_disks = db.session.query(UserDisk).filter(UserDisk.userid == current_user.id).all()
    #my_user_disks = db.session.query(UserDisk).join(DiskModel, UserDisk.diskmodelid == DiskModel.diskmodelid).filter(UserDisk.userid == current_user.id).all()
    results = db.engine.execute(text("""
        SELECT
            UD.DiskModellD,
            UD.SerialNumber,
            UD.ManufactureDate,
            DM.ManufacturerID,
            DM.CapacityBytes,
            DM.TotalDiskCount,
            DM.FailureCount,
            DM.ReliabilityScore,
            DM.Price,
            DM.URL
        FROM ss117_harddrive.userdisk UD
        JOIN ss117_harddrive.diskmodel DM ON DM.DiskModelID = UD.DiskModellD
        WHERE UD.UserID = """+str(current_user.id)+""";
    """))
    results = [row for row in results]
    return render_template('my_hard_disks.html', title = 'My Hard Disks', results = results)

@app.route("/update/<serial_number>", methods=['GET', 'POST'])
@login_required
def update_hard_disk(serial_number):
    my_user_disk = db.session.query(UserDisk).filter(UserDisk.userid == current_user.id, UserDisk.serialnumber == serial_number).first()
    form = EnterDiskModelForm()
    if form.validate_on_submit():
        my_user_disk.serialnumber = form.serial_number.data
        my_user_disk.diskmodelid = form.disk_model.data
        my_user_disk.manufacturedate = form.manufacture_date.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('my_hard_disks'))
    elif request.method == 'GET':
        form.serial_number.data = my_user_disk.serialnumber
        form.disk_model.data = my_user_disk.diskmodelid
        form.manufacture_date.data = my_user_disk.manufacturedate
    return render_template('enter_hard_disks.html', title = "Update Hard Disk", form = form)

@app.route("/delete/<serial_number>", methods=['POST'])
@login_required
def delete_hard_disk(serial_number):
    my_user_disk = db.session.query(UserDisk).filter(UserDisk.userid == current_user.id, UserDisk.serialnumber == serial_number).first()
    db.session.delete(my_user_disk)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('my_hard_disks'))

@app.route("/harddiskanalysis", methods = ['GET', 'POST'])
@login_required
def hard_disk_analysis():
    results = db.engine.execute(text("""
        SELECT
            UD.DiskModellD,
            DATE_FORMAT(DDS.Date, '%Y %m') AS YearMonth,
            SUM(DDS.FailureCount)
        FROM ss117_harddrive.userdisk UD
        JOIN ss117_harddrive.diskdailystats DDS ON DDS.DiskModelID = UD.DiskModellD
        WHERE UD.UserID = """+str(current_user.id)+"""
        GROUP BY UD.DiskModellD, DATE_FORMAT(DDS.Date, '%Y %m')
        ORDER BY UD.DiskModellD, YearMonth;
    """))
    results = [row for row in results]
    disks = [str(row[0]) for row in results]
    year_month = [str(row[1]) for row in results]
    failures = [str(row[2]) for row in results]
    results_pie = db.engine.execute(text("""
        SELECT
            UD.DiskModellD,
            DM.TotalDiskCount,
            DM.FailureCount
        FROM ss117_harddrive.userdisk UD
        JOIN ss117_harddrive.diskmodel DM ON DM.DiskModelID = UD.DiskModellD
        WHERE UD.UserID = """+str(current_user.id)+""";
    """))
    results_pie = [row for row in results_pie]
    disks_pie = [str(row[0]) for row in results_pie]
    disk_count_pie = [str(row[1]) for row in results_pie]
    failure_count_pie = [str(row[2]) for row in results_pie]
    return render_template('hard_disk_analysis.html', title = 'Hard Disk Analysis',
        disks = disks,
        year_month = year_month,
        failures = failures,
        disks_pie = disks_pie,
        disk_count_pie = disk_count_pie,
        failure_count_pie = failure_count_pie)
