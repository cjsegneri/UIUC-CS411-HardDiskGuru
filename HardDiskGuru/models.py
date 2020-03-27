from sqlalchemy.ext.automap import automap_base
from HardDiskGuru import db

# automap database tables
Base = automap_base()
Base.prepare(db.engine, reflect=True)
# DiskDailyLog = Base.classes.diskdailylog
DiskManufacturer = Base.classes.diskmanufacturer
DiskModel = Base.classes.diskmodel
User = Base.classes.user
# UserDisk = Base.classes.userdisk