# This is routes file which outlines the major routes for this application.  Login, registration, profile, index and dashboard pages. 
from flask import Blueprint, render_template, flash, redirect, url_for, request, session, current_app as app
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User
import pyodbc
from datetime import datetime
from werkzeug.security import generate_password_hash

bp = Blueprint('main', __name__)

#listed below are all the routes.  I tried to refactor this section and make it neat instead of packing all these items into the app or fun file. 
#Route for login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Here you should hash the password before checking.  I think this is a portion of the problem I am facing on login
        if authenticate_user(username, password):
            flash('Login successful!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)
#function for validating a user against the database.  _ feel like something is missing here. 
def authenticate_user(username, password):
    try:
        connection = pyodbc.connect(
            f"DRIVER={{{app.config['DRIVER']}}};"
            f"SERVER={app.config['SQL_SERVER']};"
            f"DATABASE={app.config['DATABASE']};"
            "Trusted_Connection=yes;"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT PasswordHash FROM Users WHERE Username=?", (username,))
        user = cursor.fetchone()
        connection.close()
        if user and user[0] == password:  # This should compare hashed passwords  # this was a tough one as I initially had the hash as an string, but errors were ran and I had to change it to an int. 
            return True
        return False
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        return False

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('main.login'))
    username = session['username']
    return render_template('profile.html', username=username)

@bp.route('/dashboard')
def dashboard():
    try:
        connection = pyodbc.connect(
            f"DRIVER={{{app.config['DRIVER']}}};"
            f"SERVER={app.config['SQL_SERVER']};"
            f"DATABASE={app.config['DATABASE']};"
            "Trusted_Connection=yes;"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM USERS")
        users= cursor.fetchall()

        cursor.execute("SELECT * FROM PLAYERS")
        players= cursor.fetchall()
        
        cursor.execute("SELECT * FROM PARENTS")
        parents= cursor.fetchall()

        cursor.execute("SELECT * FROM COACHES")
        coaches= cursor.fetchall()

        connection.close()

        return render_template('dashboard.html', users=users, players=players, parents=parents, coaches=coaches)
    except pyodbc.Error as e:
        print(f"Databse connection failed: {e}")
        flash('An error occurred and dashboard information could not be displayed. Try again at a later time.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        email = form.email.data
        role = form.role.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        date_of_birth = form.date_of_birth.data
        team_id = form.team_id.data if form.team_id.data else None
        contact_number = form.contact_number.data
        address = form.address.data if form.address.data else None
       
        try:
            date_of_birth_str = date_of_birth.strftime('%Y-%m-%d') if date_of_birth else None
            connection = pyodbc.connect(
                f"DRIVER={{{app.config['DRIVER']}}};"
                f"SERVER={app.config['SQL_SERVER']};"
                f"DATABASE={app.config['DATABASE']};"
                "Trusted_Connection=yes;"
            )
            cursor = connection.cursor()
            cursor.execute("{CALL AddUserAndRelatedInfo (?, ?, ?, ?, ?, ?, ?, ?, ?, ? )}", 
                username, password, email, role, first_name, last_name, date_of_birth_str, team_id,
                contact_number, address
            )
            connection.commit()
            connection.close()
            flash('Registration successful!', 'success')
            return redirect(url_for('main.profile'))
        except pyodbc.Error as e:
            print(f"Database connection failed: {e}")
            flash('An error occurred while registering. Please try again.', 'danger')
    return render_template('register.html', form=form)
