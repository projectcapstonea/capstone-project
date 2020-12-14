from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from project import db
from project.models import CustomerData

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) # StringField('[label]', list of instanced validators')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_pass', message='Passwords do not match')])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    dob = DateField('DOB', validators=[DataRequired()])
    str = StringField('Street', validators=[DataRequired()])
    cty = StringField('City', validators=[DataRequired()])
    trty = StringField('Territory', validators=[DataRequired()])
    ctry = StringField('Country', validators=[DataRequired()])
    intr = SelectField('Interests', choices=[(q[0], q[0]) for q in db.session.query(CustomerData.int).distinct()])
    pers = SelectField('Personality', choices=[(q[0], q[0]) for q in db.session.query(CustomerData.per).distinct()])
    pref = BooleanField('Email Preference',validators=None)
    submit = SubmitField('Register')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email has already been registered')

class RecommendationForm(FlaskForm):
    place = SelectField('Restaurant', choices=[(q[1], q[0]) for q in db.session.execute("SELECT name, placeID FROM RestaurantFeatureData ORDER BY name")])
    rating = SelectField('Rating', choices=[('0', '0'), ('1', '1'), ('2', '2')])
    submit = SubmitField('Submit')

class RatingForm(FlaskForm):
    restaurant = SelectField('Restaurant', choices=[(q[1], q[0]) for q in db.session.execute("SELECT name, placeID FROM RestaurantFeatureData ORDER BY name")])
    rating = SelectField('Rating', choices=[('0', '0'), ('1', '1'), ('2', '2')])
    submit = SubmitField('Submit')
