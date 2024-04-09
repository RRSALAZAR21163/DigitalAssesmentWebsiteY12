from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password1) < 8:
            flash('Password must have at least 8 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        else:
            flash('Account created!', category='success')
        
    return render_template("signup.html")
