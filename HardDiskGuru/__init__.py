from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecef3b8e7d47ea8a26b098bc534393dd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ss117_hard_disk_guru_web:DatabasePassword@localhost/ss117_harddrive'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from HardDiskGuru import routes