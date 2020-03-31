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

Base.prepare(db.engine, reflect=True)
# DiskDailyLog = Base.classes.diskdailylog
DiskManufacturer = Base.classes.diskmanufacturer
DiskModel = Base.classes.diskmodel
#User = Base.classes.user
# UserDisk = Base.classes.userdisk