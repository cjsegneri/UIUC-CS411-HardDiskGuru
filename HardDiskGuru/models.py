from sqlalchemy.ext.automap import automap_base
from HardDiskGuru import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == int(user_id)).first()

# automap database tables
Base = automap_base()

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = db.Column('UserID', db.Integer, primary_key=True)
    email = db.Column('Email', db.String)
    password = db.Column('Password', db.String)

class DiskManufacturer(Base, UserMixin):
    __tablename__ = 'diskmanufacturer'

    manufacturerid = db.Column('ManufacturerID', db.String, primary_key = True)

class DiskModel(Base, UserMixin):
    __tablename__ = 'diskmodel'

    diskmodelid = db.Column('DiskModelID', db.String, primary_key=True)
    manufacturerid = db.Column('ManufacturerID', db.String)
    capacitybytes = db.Column('CapacityBytes', db.BigInteger)
    totaldiskcount = db.Column('TotalDiskCount', db.Integer)
    failurecount = db.Column('FailureCount', db.Integer)

class UserDisk(Base, UserMixin):
    __tablename__ = 'userdisk'

    userid = db.Column('UserID', db.Integer, primary_key=True)
    diskmodelid = db.Column('DiskModellD', db.String)
    serialnumber = db.Column('SerialNumber', db.String, primary_key=True)
    manufacturedate = db.Column('ManufactureDate', db.DateTime)

Base.prepare(db.engine, reflect=True)
