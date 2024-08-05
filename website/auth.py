### IMPORTS from Modules ###
from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db #import database

auth = Blueprint("auth", __name__)


# Login route
@auth.route("/login", methods = ['GET', 'POST'])
def login(): #define the function
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Signup route
@auth.route("/signup", methods = ['GET', 'POST'])
def sign_up():  #define the function
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 8:
            flash('Password must have at least 8 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password = generate_password_hash(password1, method='scrypt:32768:8:1'))
            db.session.add(new_user) # add something to database
            db.session.commit() #commit to database
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("signup.html", user=current_user)

#Logout route
@auth.route("/logout")
@login_required #authentication/user is logged in is required to access this page
def logout():  #define the function
    logout_user()
    flash('You have logged out Successfully!', category='success')
    return redirect(url_for('auth.login'))