from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) # StringField('[label], list of instanced validators'
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_pass', message='Passwords do not match')])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    dob = StringField('DOB', validators=[DataRequired()])
    str = StringField('Street', validators=[DataRequired()])
    cty = StringField('City', validators=[DataRequired()])
    trty = StringField('Territory', validators=[DataRequired()])
    ctry = StringField('Country', validators=[DataRequired()])
    intr = StringField('Interests', validators=[DataRequired()])
    pers = StringField('Personality', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email has already been registered')


