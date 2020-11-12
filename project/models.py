from project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'tblUsers'
    id = db.Column('ID', db.Integer, primary_key = True)
    fname = db.Column('FirstName', db.String)
    lname = db.Column('LastName', db.String)
    email = db.Column('Email', db.String)
    dob = db.Column('DOB', db.Date)
    str = db.Column('Street', db.String)
    city = db.Column('City', db.String)
    trty = db.Column('Territory', db.String)
    ctry = db.Column('Country', db.String)
    int = db.Column('Interests', db.String)
    per = db.Column('Personality', db.String)
    code = db.Column('Password', db.String)
    lat = db.Column('Latitude', db.String)
    lon = db.Column('Longitude', db.String)

    def __init__(self, fname, lname, email, dob, str, city, trty, ctry, int, per, code, lat, lon):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.dob = dob
        self.str = str
        self.city = city
        self.trty = trty
        self.ctry = ctry
        self.int = int
        self.per = per
        self.code = generate_password_hash(code)
        self.lat = lat
        self.lon = lon

    def check_password(self, code):
        return check_password_hash(self.code, code)



