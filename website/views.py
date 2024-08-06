### IMPORTS From Modules ###
from flask import Blueprint, render_template, url_for, request, redirect, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Note, Post, Comment, Like
import json
from . import db #import database

views = Blueprint('views', __name__)

### Basic Layout ###
#route
#define function
#return. The template that will be rendered for the page.

#HOME ROUTE
#USER HAS TO BE AUTHENTICATED TO ACCESS
@login_required #authentication/user is logged in is required to access this page
@views.route("/") #routes
@views.route("/home") #ROUTES
def home(): #define the function
    return render_template("home.html", user=current_user) #render template home.html

#DASHBOARD ROUTE
@views.route("/dashboard", methods = ['GET', 'POST']) #Method is GET and POST. To get details from database and to post/update details to database. ROUTES
@login_required #authentication/user is logged in is required to access this page
def dashboard(): #define the function
    if request.method == 'POST': #request 
        note = request.form.get('note') #Gets the note from the HTML
        if len(note) < 1: #if the input of letters or words is less than one
            flash('Note is too short!', category='error') #Flash message
        else:
            new_note = Note(data=note, user_id=current_user.id) #providing the schema for the note
            db.session.add(new_note) #adding the note to the database
            db.session.commit()  #commit to database
            flash('Note added!', category='success') #Flash message
    return render_template("dashboard.html", user=current_user) #render template dashboard.html

#DELETING NOTES ROUTE
@views.route('/delete-note', methods=['POST']) #Method is POST. Update detail/informations on database. ROUTES
def delete_note(): #define the function
    note = json.loads(request.data) #variable
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id: #if user is the creater user can delete
            db.session.delete(note) # delete something to database
            db.session.commit()  #commit to database
            #flash
            flash('Note deleted!', category='success') #Flash message
    return jsonify({})

#BLOG ROUTE
@views.route("/blogs", methods = ['GET', 'POST']) #Method is GET and POST. ROUTES
@login_required
def blog(): #define the function
    posts = Post.query.all() #display posts
    return render_template("blogs.html", user=current_user, posts=posts) #render template blogs.html


#CREATE POST
@views.route("/create-post", methods=['GET', 'POST']) #Method is GET and POST. To get details from database and to post/update details to database. ROUTES
@login_required #authentication/user is logged in is required to access this page
def create_post(): #define the function
    if request.method == "POST": #POST
        text = request.form.get('text') #form. 'Text'

        if not text: #if the post is empty
            flash('Post cannot be empty', category='error') #Flash message
        else: 
            post = Post(text=text, author=current_user.id) #create new post. Matches the author id with current user id
            db.session.add(post) # add something to database
            db.session.commit()  #commit to database
            flash('Post created!', category='success') #Flash message
            return redirect(url_for('views.blog'))

    return render_template('addblogs.html', user=current_user) #render template addblogs.html

#DELETING POSTSS
@views.route("/delete-post/<id>") # ROUTES
@login_required #authentication/user is logged in is required to access this page
def delete_post(id): #define the function
    post = Post.query.filter_by(id=id).first()

    if not post: #post not existing
        flash("Post does not exist.", category='error') #Flash message
    elif current_user.id != post.author: #if current user id is = to the post.author.
        flash('You do not have permission to delete this post.', category='error') #Flash message
    else:
        db.session.delete(post) # delete something to database
        db.session.commit()  #commit to database
        flash('Post deleted.', category='success') #Flash message

    return redirect(url_for('views.blog')) #redirect to views.blog

# USER SPECIFIC PAGE ROUTE.
@views.route("/posts/<username>") # ROUTES
@login_required #authentication/user is logged in is required to access this page
def posts(username): #define the function
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error') #Flash message
        return redirect(url_for('views.home')) #redirect back to home page
    posts = user.posts
    return render_template("userposts.html", user=current_user, posts=posts, username=username) #render template userposts.html

#CREATING COMMENTS 
@views.route("/create-comment/<post_id>", methods=['POST']) #Method is POST. Update details on database. ROUTES
@login_required #authentication/user is logged in is required to access this page
def create_comment(post_id): #define the function
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error') #Flash message
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id) #create new comment
            db.session.add(comment) # add something to database
            db.session.commit()  #commit to database
            flash('Post created!', category='success') #Flash message
        else:
            flash('Post does not exist.', category='error') #Flash message

    return redirect(url_for('views.blog')) #redirect to views.blogs

#DELETEING COMMENTS
@views.route("/delete-comment/<comment_id>")#ROUTES
@login_required #authentication/user is logged in is required to access this page
def delete_comment(comment_id): #define the function
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')  #Flash message. Error message
    elif current_user.id != comment.author and current_user.id != comment.post.author: #checks if userid does not equals to comment.author and userid does not equal commentpostauthor.
        flash('You do not have permission to delete this comment.', category='error') #Flash message
    else:
        db.session.delete(comment) #delete something to database
        db.session.commit()  #commit to database
        flash('Post deleted.', category='success') #Flash message

    return redirect(url_for('views.blog')) #redirect to views.blog

#LIKING POSTS
@views.route("/like-post/<post_id>", methods=['POST']) #Method is POST. Update details on Database. ROUTES
@login_required #authentication/user is logged in is required to access this page
def like(post_id): #define the function
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400) #Sends Error if Post does not exist
    elif like:
        db.session.delete(like) # delete something to database
        db.session.commit() #commit to database
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like) # add something to database
        db.session.commit() #commit to database

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)}) #return jsonify likes.