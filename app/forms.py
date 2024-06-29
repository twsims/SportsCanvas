# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('Parent', 'Parent'), ('Player', 'Player'), ('Coach', 'Coach')], validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()], default=None)
    team_id = StringField('Team ID', validators=[Length(max=10)], default=None)
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=15)])
    address = StringField('Address', validators=[Length(max=255)], default=None)
    submit = SubmitField('Register')