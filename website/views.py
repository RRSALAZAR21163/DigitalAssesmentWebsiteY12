from flask import Blueprint, render_template, url_for, request, redirect, flash, jsonify
from flask_login import login_required, current_user
from .models import User
from .models import Post
from . import db
import json

views = Blueprint('views', __name__)

@login_required
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/blogs", methods = ['GET', 'POST'])
def blog():
    posts = Post.query.all()
    return render_template("blogs.html", user=current_user, posts=posts)
    
@views.route("/create-post", methods = ['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog'))
    return render_template('addblogs.html', user=current_user)

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)