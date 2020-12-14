from project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'RegisteredUsers'
    id = db.Column('ID', db.String , primary_key = True)
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
    pref = db.Column('EmailPreference', db.SmallInteger)

    def __init__(self, id, fname, lname, email, dob, str, city, trty, ctry, int, per, code, lat, lon, pref):
        self.id = id
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
        self.pref = pref

    def check_password(self, code):
        return check_password_hash(self.code, code)

class UserRatings(db.Model):
    __tablename__ = 'UserRestaurantRatings'
    id = db.Column('userID', db.String, primary_key = True)
    place = db.Column('placeID', db.Integer, primary_key = True)
    rating = db.Column('rating', db.String)

    def __init__(self, id, place, rating):
        self.id = id
        self.place = place
        self.rating = rating

class CustomerData(db.Model):
    __tablename__ = 'RestaurantCustomerData'
    id = db.Column('userID', db.String, primary_key = True)
    lat = db.Column('latitude', db.Float)
    lon = db.Column('longitude', db.Float)
    smoker = db.Column('smoker', db.String)
    drink = db.Column('drink_level', db.String)
    dress = db.Column('dress_preference', db.String)
    amb = db.Column('ambience', db.String)
    tran = db.Column('transport', db.String)
    mar = db.Column('marital_status', db.String)
    child = db.Column('hijos', db.String)
    dob = db.Column('birth_year', db.Integer)
    int = db.Column('interest', db.String)
    per = db.Column('personality', db.String)
    rel = db.Column('religion', db.String)
    act = db.Column('activity', db.String)
    col = db.Column('color', db.String)
    wght = db.Column('weight', db.String)
    budget = db.Column('budget', db.String)
    hght = db.Column('height', db.String)

    def __init__(self, id, lat, lon, smoker, drink, dress, amb, tran, mar, child, dob, int, per, rel, act, col, wght, budget, hght):
        self.id = id
        self.lat = lat
        self.smoker = smoker
        self.drink = drink
        self.dress = dress
        self.amb = amb
        self.tran = tran
        self.mar = mar
        self.child = child
        self.dob = dob
        self.int = int
        self.per = per
        self.rel = rel
        self.act = act
        self.col = col
        self.wght = wght
        self.budget = budget
        self.hght = hght

class RestaurantData(db.Model):
    __tablename__ = 'RestaurantFeatureData'
    id = db.Column('placeID', db.Integer, primary_key = True)
    lat = db.Column('latitude', db.Float)
    lon = db.Column('longitude', db.Float)
    geom = db.Column('the_geom_meter', db.String)
    name = db.Column('name', db.String)
    addr = db.Column('address', db.String)
    cty = db.Column('city', db.String)
    state = db.Column('state', db.String)
    ctry = db.Column('country', db.String)
    fax = db.Column('fax', db.String)
    zip = db.Column('zip', db.Integer)
    alc = db.Column('alcohol', db.String)
    smk = db.Column('smoking_area', db.String)
    dress = db.Column('dress_code', db.String)
    acc = db.Column('accessibility', db.String)
    price = db.Column('price', db.String)
    url = db.Column('url', db.String)
    amb = db.Column('Rambience', db.String)
    fran = db.Column('franchise', db.String)
    area = db.Column('area', db.String)
    serv = db.Column('other_services', db.String)

    def __init__(self, id, lat, lon, geom, name, addr, cty, state, ctry, fax, zip, alc, smk, dress, acc, price, url, amb, fran, area, serv):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.geom = geom 
        self.name = name
        self.addr = addr
        self.cty = cty
        self.state = state
        self.ctry = ctry
        self.fax = fax
        self.zip = zip
        self.alc = alc
        self.smk = smk
        self.dress = dress
        self.acc = acc
        self.price = price
        self.url = url
        self.amb = amb
        self.fran = fran
        self.area = area
        self.serv = serv
