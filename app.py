from smithsonian_api import search, format_images, ApiImage
import requests
import random
import simplejson as json
# import pdb

from flask import Flask, render_template, request, flash, redirect, session, g, abort, url_for, Markup, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from flask.sessions import SecureCookieSessionInterface

def user_loaded_from_header(self, user=None):
    g.login_via_header = True

from user_form import LoginForm, RegisterForm
from secure import secret_key
from models import User, connect_db, db, Image, Like
from seed import seed_database
from smithsonian_api import search, format_images, ApiImage

app = Flask(__name__)
# pdb.set_trace()


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///smithsonian'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY']= secret_key

Bootstrap(app)
toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"
# test images for api response
DEV = True
DEBUG = False

if DEBUG:
   seed_database()
else:
   db.create_all()

API_BASE_URL = 'https://api.si.edu/openaccess/api/v1.0/search'


@app.route('/')
@app.route('/login')
@app.route('/register')


def homepage():
   '''Render homepage'''
   
   form = LoginForm()
   req = request.path 
   
   if req == "/register": 
      form = RegisterForm()
      req = "register"
   else:
      req = "login"
   
   formatted_images = search(search_terms="None", dev=DEV, images_per_row=9, max_rows=1, max_results=9)

   return render_template('homepage.html', formatted_images=formatted_images, form=form, req=req)


@app.route('/register', methods=['POST'])
def register():
   '''Register new user'''
   
   form = RegisterForm()
   try:
      if form.validate_on_submit():

         username=form.username.data
         email=form.email.data   
         password = form.password.data

         user = User.create(username=username, email=email, password=password)
         db.session.commit()
         flash('Account created', 'success')
         return redirect(f'/profile/{username}')
      else: 
         flash('Registration unsuccessful', 'danger')
         return redirect('/')
      
   except IntegrityError as e:
      flash('Sorry that username is already taken. Please enter a new username')
      return redirect('/')
   
@app.route('/login', methods=['POST'])
def login():
   '''Login returning user.'''
   
   form = LoginForm()

   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      user = User.query.filter_by(username=username).first()
      user = User.authenticate(username=username, password=password)
      if user:         
         User.user_login(user.username)
         return redirect(f'/profile/{user.username}')
      else: 
         flash('Username and password not found', 'warning')
   else:
      flash('Login unsuccessful, please resubmit. If you do not already\
         have an account please register to join.', 'danger')
      return redirect('/')
   

@app.route("/profile/<username>")
def show_user(username):   
   """Render user information and hompage boards"""
   
   if User.verify_login():

      user = User.query.filter_by(username=username).first()
      print(user)

      formatted_images = search('"data_source="American Art&painting"',
                        max_results=12, images_per_row=6, max_rows=2, dev=DEV)

      return render_template('user/profile.html', formatted_images=formatted_images, user=user)
     

@app.route("/user/<username>/search", methods=["GET", "POST"])
def user_search(username):
   """User search and display results."""
   
   if User.verify_login():
      
      keyword = request.form.get('keyword')
      
      user = User.query.filter_by(username=username).first()
      
      formatted_images = search(
            search_terms=keyword, max_results=12, dev=DEV, images_per_row=6, max_rows=2)
      
      return render_template('user/search.html', formatted_images=formatted_images, user=user)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
   '''Logout user.'''
  
   if CURR_USER_KEY in session:
       del session[CURR_USER_KEY]
       flash('You are now logged-out.', 'success')
   return redirect('/')


@app.route('/api/<user_id>/like', methods=["POST"])
def add_like(user_id):
    '''Add liked image to database.'''

    data = request.json
   
    image = Image(
        url=data['url'],
        title=data['title'],
        artist=data['artist'],
        date=data['date'],
        collection=data['collection']
    )

    db.session.add(image)
    db.session.commit()

   #  liked_image = Image.query.filter(Image.like(f"%{image.url}")).all()
    liked_image = Image.query.filter_by(url=image.url).all()
    
    user = User.query.get_or_404(user_id)
      
    like = Like(
        user_id=user.id,
        image_id=liked_image[0].id
    )
    
    db.session.add(like)
    db.session.commit()
    
    # return HTTP status of created
    flash('Added', 'success')
    return ('201')
 

@app.route('/api/<user_id>/unlike', methods=["POST"])
def unlike(user_id):
    '''Removed liked image from database.'''
    
    data = request.json
    
    url = data['url']
    
    unlike_images = Image.query.filter_by(url=url).all()
    for image in unlike_images:
       row = Like.query.filter_by(user_id=user_id,
                                  image_id=image.id).first()
       
       
       db.session.delete(row)
    
    db.session.commit()
    flash('Removed', 'success')
    return ('201')
 
@app.route('/api/<user_id>/likes') 
def get_likes(user_id):
   '''Get user likes.'''
    
   user = User.query.get_or_404(user_id)

   user = User.query.get_or_404(user_id)
   user_likes = user.likes
   
   formatted_likes = []

   for image in user_likes:
      formatted_img = {
                        'url': user.likes[0].url, 
                        'title': user.likes[0].title, 
                        'artist': user.likes[0].artist, 
                        'date': user.likes[0].date, 
                        'medium': None,
                        'collection': user.likes[0].collection, 
                        'raw_response': None}
      formatted_likes.append(formatted_img)
   
   response = formatted_likes
   response = jsonify(response)

   return (response)
    

if __name__ == "__main__":
     app.run(debug=True)


