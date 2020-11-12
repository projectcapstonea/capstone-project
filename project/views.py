from flask import render_template
from project import app, db
import time
from geopy.geocoders import Nominatim
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from project.models import User
from project.forms import LoginForm, RegistrationForm

map = Nominatim(user_agent="ifood")

def get_coordinates(address):
    time.sleep(1)
    try:
        return map.geocode(address).raw
    except:
        return get_coordinates(address)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home Page')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully')
            next = request.args.get('next') # Saves request for initial page, redirects to login and after authentication then redirects to that page
            if next == None or not next[0]=='/':
                next = url_for('welcome')
            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        location = get_coordinates(form.str.data + ', ' + form.cty.data + ', ' + form.trty.data + ', ' + form.ctry.data)
        user = User(email=form.email.data,
                    code=form.confirm_pass.data,
                    fname=form.fname.data,
                    lname=form.lname.data,
                    dob=form.dob.data,
                    str=form.str.data,
                    city=form.cty.data,
                    trty=form.trty.data,
                    ctry=form.ctry.data,
                    int=form.intr.data,
                    per=form.pers.data,
                    lat=location["lat"],
                    lon=location["lon"]
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)