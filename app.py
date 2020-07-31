# TODO: rework flask-login all functions including - CustomSessionInterface()
# TODO: troubleshoot cookies and is_safe_URL 
# https://flask-login.readthedocs.io/en/latest/login-example
# https://hackersandslackers.com/flask-login-user-authentication/
# https://flask-login.readthedocs.io/en/latest/_modules/flask_login/login_manager.html



# TODO: update dependencies


import requests
import random


from flask import Flask, render_template, request, flash, redirect, session, g, abort, url_for, Markup
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
import simplejson as json
from flask.sessions import SecureCookieSessionInterface
from werkzeug.security import generate_password_hash, check_password_hash


def user_loaded_from_header(self, user=None):
    g.login_via_header = True


from user_form import LoginForm, RegisterForm
from secure import secret_key
from models import User, connect_db, db, User, Board, Image, Like, Follow, Like
from seed import seed_database
from smithsonian_api import search, format_images

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///smithsonian'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY']= secret_key

Bootstrap(app)
toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"
DEBUG = True
DEV = True

if DEBUG:
   seed_database()
else:
   db.create_all()

API_BASE_URL = 'https://api.si.edu/openaccess/api/v1.0/search'


@app.route('/')
@app.route('/login')
@app.route('/register')

# TODO: add JS for event listener to direct to section on homepage
def homepage():
   '''Render homepage'''
   
   if User.verify_login():
      return redirect(f"/profile/{session['CURR_USER']}")
   
   form = LoginForm()
   req = request.path 
   
   if req == "/register": 
      form = RegisterForm()
      req = "register"
   else:
      req = "login"
   
   formatted_images = search('"data_source="American Art&painting"', dev=DEV, images_per_row=9, max_rows=1, max_results=9)

   return render_template('homepage.html', formatted_images=formatted_images, form=form, req=req)

# ********* USER ROUTES *********

@app.route('/register', methods=['POST'])
def register():
   '''Register new user'''
   
   # if User.verify_login():
   #    return redirect(f"/profile/{session['CURR_USER']}")
   
   form = RegisterForm()

   if form.validate_on_submit():

      username=form.username.data
      email=form.email.data   
      password = form.password.data

      user = User.create(username=username, email=email, password=password)
      db.session.commit()
      flash('Welcome! Your account had been created.', 'success')
      return redirect(f'/profile/{username}')

      # else: 
      #    flash('Registration unsuccessful, Please resubmit. If you already have an account please login.', 'warning')

   else: 
      return redirect('/')


@app.route('/login', methods=['POST'])
def login():
   '''Login returning user.'''
   
   # if User.verify_login():
   #    return redirect(f"/profile/{session['CURR_USER']}")
   
   form = LoginForm()

   if form.validate_on_submit():
      username = form.username.data
      user = User.query.filter_by(username=username).first()
      if user:
         if check_password_hash(user.password, form.password.data):
            User.user_login(user.username)
            return redirect(f'/profile/{user.username}')
         else: 
            flash('Username and password not found', 'warning')
   else:
      flash('Login unsuccessful, please resubmit. If you do not already\
         have an account please register to join.', 'warning')
      return redirect('/')
   

# route for user boards - verify with login_required
@app.route("/profile/<username>")
def show_user(username):   
   """Render user information and hompage boards"""

   username = User.query.filter_by(username=username).first()

   formatted_images = search('"data_source="American Art&painting"',
                     max_results=12, images_per_row=6, max_rows=2, dev=DEV)

   return render_template('profile.html', formatted_images=formatted_images, user=user)
     
   

@app.route("/user/likes/<int:user_id>")
def show_likes(user_id):
   """Render user likes."""
   
   # username = User.verify_login()
   # if not username:
   #    return redirect('/')
   
   if session.get(CURR_USER_KEY, False):

      user = User.query.get(session[CURR_USER_KEY])

      if user:
         image_urls = ['https://images.unsplash.com/photo-1595970331019-3b2bc16e9890?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=60']
         return render_template('likes.html', image_urls=image_urls, user=user, dev=True, images_per_row=6, max_rows=2, max_results=24)

 
@app.route("/user/following/<int:user_id>")
def show_following(user_id):
   """Render user following."""
   if session.get(CURR_USER_KEY, False):
      
      user = User.query.get(session[CURR_USER_KEY])
   
      if user:
         image_urls = [
              'https://images.unsplash.com/photo-1595970331019-3b2bc16e9890?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=60']
         return render_template('following.html', image_urls=image_urls, user=user, dev=True,  images_per_row=6, max_rows=2, max_results=24)


@app.route("/user/search", methods=["GET", "POST"])
def user_search():

   # if User.verify_login():
   keyword = request.form.get('keyword')
   formatted_images = search(
         search_terms=keyword, max_results=12, dev=DEV, images_per_row=6, max_rows=2)
   

   return render_template('user/search.html', formatted_images=formatted_images, user=user)
   # else:
   #    return redirect('/')

@app.route("/logout", methods=['GET', 'POST'])
# @login_required
def logout():
   '''Logout user.'''
  
   if CURR_USER_KEY in session:
       del session[CURR_USER_KEY]
       flash('You are now logged-out.', 'success')
       
# TODO:   return render_template('user/logout.html')
   return redirect('/')


if __name__ == "__main__":
     app.run(debug=True)
