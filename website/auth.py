### IMPORTS from Modules ###
from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db #import database

auth = Blueprint("auth", __name__)


# Login route
@auth.route("/login", methods = ['GET', 'POST']) #Method is GET and POST To get details from database and to post/update details to database. ROUTES
def login(): #define the function
    if request.method == 'POST':
        email = request.form.get('email') #get details from database
        password = request.form.get('password') #get details from database
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success') #Flash message
                login_user(user, remember=True) #remember user if user logs in
                return redirect(url_for('views.dashboard')) #redirect back to dashboard page when user logs in
            else:
                flash('Incorrect password, try again.', category='error') #Flash message
        else:
            flash('Email does not exist.', category='error') #Flash message

    return render_template("login.html", user=current_user)

# Signup route
@auth.route("/signup", methods = ['GET', 'POST']) #Method is GET and POST. To get details from database and to post/update details to database. ROUTES
def sign_up():  #define the function
    if request.method == 'POST': #Post. Update these details to the database
        email = request.form.get('email')
        username = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    
        user = User.query.filter_by(email=email).first() 
        if user:
            flash('Email already exists.', category='error') #Flash message
        elif len(email) < 4: #if email is less than 3 characters
            flash('Email must be greater than 3 characters.', category='error') #Flash message
        elif len(username) < 2: #if username is less than 1 character
            flash('First name must be greater than 1 character.', category='error') #Flash message
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 8: #passwords must have atleast 8 characters
            flash('Password must have at least 8 characters.', category='error') #Flash message
        else:
            new_user = User(email=email, username=username, password = generate_password_hash(password1, method='scrypt:32768:8:1')) #generate a hashed password. Encrypt the password
            db.session.add(new_user) # add something to database
            db.session.commit() #commit to database
            login_user(new_user, remember=True) #if new user create a new user, and remember
            flash('Account created!', category='success') #Flash message 
            return redirect(url_for('views.home'))
    
    return render_template("signup.html", user=current_user)

#Logout route
@auth.route("/logout") #ROUTES
@login_required #authentication/user is logged in is required to access this page
def logout():  #define the function
    logout_user() #logout the user function
    flash('You have logged out Successfully!', category='success') #Flash message 
    return redirect(url_for('auth.login')) #redirect back to login page