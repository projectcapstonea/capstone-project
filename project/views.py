from project import app, db, mail
import time
from geopy.geocoders import Nominatim
from flask import render_template, redirect, request, url_for, flash, abort, Response
from flask_login import login_user, login_required, logout_user, current_user
from project.models import User, UserRatings, CustomerData, RestaurantData
from project.forms import LoginForm, RegistrationForm, RecommendationForm, RatingForm
from sqlalchemy import create_engine, func
from flask_mail import Message
import urllib.request
import json
from os.path import join, dirname

map = Nominatim(user_agent="ifood")

# Function to retrieve coordinates of users' address
def get_coordinates(address):
    time.sleep(1)
    try:
        return map.geocode(address).raw
    except:
        return get_coordinates(address)

# Function to continue sequence of ID in the format Uxxxx
def get_last_userid():    
    query = db.session.query(User).first()
    if query is None:
        max_id = 'U' + str(int(db.session.query(func.max(CustomerData.id)).scalar().replace('U', '')) + 1)
    else:
        max_id = 'U' + str(int(db.session.query(func.max(User.id)).scalar().replace('U', '')) + 1)
    return max_id

# Welcome email
def welcome_email(username, email):
    path = join(dirname(__file__), 'static\img\logo.png')
    msg = Message("Welcome to iFood!", recipients=[email])
    msg.attach('logo.png', 'image/png', open(path, 'rb').read(), 'inline', headers=[['Content-ID', 'logo'],])
    msg.html = "<h3>Hello " + username + "!</h> \
                <p> We are excited to welcome you to our platform! </p> \
                <p> We sincerely hope this is the beginning of a mutually beneficial relationship. </p> \
                <p> Check our quick start guides so you can get up and running as soon as possible. </p> \
                <p> Keep safe and happy eating! </p> \
                <p>The iFood Team </p>\
                <img src=\"cid:logo\"> \
                "
    mail.send(msg)

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
        user = User(
                    id = get_last_userid(),
                    email=form.email.data,
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
                    lon=location["lon"],
                    pref=form.pref.data
                    )
        db.session.add(user)
        db.session.commit()
        welcome_email(user.fname, user.email)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/recommendation', methods=['GET', 'POST'])
@login_required
def recommendation():
    form = RecommendationForm()
    recommendations = {}
    place = []
    if form.validate_on_submit():
        data = {
            "Inputs": {
                "input1":
                [
                    {
                        'userID': current_user.id,   
                        'placeID': form.place.data,   
                        'rating': form.rating.data,  
                    }
                ],
                },
            "GlobalParameters":  {
                }
            }
        body = str.encode(json.dumps(data))
        url = 'https://ussouthcentral.services.azureml.net/workspaces/5559fed4330c4fe28597147032c1b7a2/services/84d1a8f7ee824fd3966e95c90cd9b6d7/execute?api-version=2.0&format=swagger'
        api_key = 'ntzC50GbvMRY6KGiU99LehNNUFzWAYzApjVnMoPCqm31m0Dk5JpBksnzhrFudEYriFGAH+P0tzFYG4nfosHIvw=='
        
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
        req = urllib.request.Request(url, body, headers)
        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            output = json.loads(result)
            for k, v in output['Results']['output1'][0].items():
                recommendations.update({k: v})
            recommendations.pop("User")
            for k, v in recommendations.items():
                place.append(db.session.query(RestaurantData.name).filter(RestaurantData.id == v).scalar())
            return render_template('results.html', form=form, place=place)
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))
            print(error.info())
            print(json.loads(error.read().decode("utf8", 'ignore')))
            return render_template('recommendation.html', form=form, error=error)

    return render_template('recommendation.html', form=form)

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    return render_template('results.html')

@app.route('/toprated', methods=['GET', 'POST'])
@login_required
def toprated():
    result = {}
    form = RecommendationForm()
    data = db.session.execute("SELECT rf.name, [Average Rating] FROM TopRatedRestaurants AS vw INNER JOIN RestaurantFeatureData as rf ON vw.placeID = rf.placeID")
    for row in data:
        result.update({row[0]: round(row[1], 1)})
    data.close()

    return render_template('toprated.html', form=form, result=result)

@app.route('/rating', methods=['GET', 'POST'])
@login_required
def rating():
    form = RatingForm()
    if form.validate_on_submit():
        rating = UserRatings(id = current_user.id, place = int(form.restaurant.data), rating = form.rating.data)
        db.session.add(rating)
        db.session.commit()
        return redirect(url_for('recommendation'))
    return render_template('rating.html', form=form)
