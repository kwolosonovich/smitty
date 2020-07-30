# TODO: rework flask-login all functions including - CustomSessionInterface()
# TODO: troubleshoot cookies and is_safe_URL 
# https://flask-login.readthedocs.io/en/latest/login-example
# https://hackersandslackers.com/flask-login-user-authentication/
# https://flask-login.readthedocs.io/en/latest/_modules/flask_login/login_manager.html



# TODO: update dependencies


import requests

from flask import Flask, render_template, request, flash, redirect, session, g, abort, url_for, Markup
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap 
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user
from flask_wtf import FlaskForm
import simplejson as json
from flask.sessions import SecureCookieSessionInterface
# from jinja2 import Environment, select_autoescape


def user_loaded_from_header(self, user=None):
    g.login_via_header = True


from user_form import LoginForm, RegisterForm
from secure import secret_key
from models import User, connect_db, db, User, Board, Image, Like, Follow, Like
from seed import seed_database
from smithsonian_api import search

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///smithsonian'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY']= secret_key


toolbar = DebugToolbarExtension(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Bootstrap(app)
connect_db(app)

# disable session cookie for APIs
# TODO: need to resolve errors
# class CustomSessionInterface(SecureCookieSessionInterface):
#     """Prevent creating session from API requests."""

#     def save_session(self, *args, **kwargs):
#         if User.get('login_via_header'):
#             return
#         return super(CustomSessionInterface, self).save_session(*args, **kwargs)

# app.session_interface = CustomSessionInterface()

# @user_loaded_from_header.connect
# def user_loaded_from_header(self, user=None):
#     User.login_via_header = True
# enable configure session protection

login_manager.session_protection = "strong"


DEBUG = True

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
   
   if current_user.is_authenticated:
      return redirect('/user/profile')
   
   form = LoginForm()
   req = request.path 
   
   if req == "/register": 
      form = RegisterForm()
   else:
      req = "/login"

   # TODO: add logic to prevent new images search call   
   images = search('"data_source="American Art&painting"', 9)

   return render_template('homepage.html', image_urls=images, form=form, req=req)

# ********* USER ROUTES *********


@app.route('/register', methods=['POST'])
def register():
   '''Register new user'''
   # global STATUS
   # STATUS = 'register'

   form = RegisterForm()
   
   if form.validate_on_submit():

      username=form.username.data
      email=form.email.data
      profile_image=form.profile_image.data
      backdrop_image=form.backdrop_image.data
      password=form.password.data

      user = User.create(username, email, profile_image, backdrop_image, password)

      db.session.commit()
      login_user(user)
      flash('Welcome! Your account had been created.', 'success')
   
   
   # TODO: troubleshoot is_safe_URL https://flask-login.readthedocs.io/en/latest/login-example
      # check if the url is safe for redirects
      # next = request.args.get('/user/profile')
      # if not is_safe_url(next):
      #     return flask.abort(400)
      # else: 
      return redirect('/user/profile')
   
# TODO: flash('Registration unsuccessful, Please resubmit. If you already have an account please login.', 'warning')
   return redirect('/') 

@app.route('/login', methods=['POST'])
def login():
   '''Login returning user.'''
   
   print(request)
   
   form = LoginForm()

   if form.validate_on_submit():
      
      user = User.authenticate(form.username.data,
                         form.password.data)
      
      # user = User.is_authenticate(form.username.data, 
      #                          form.password.data)

      # authenticate user name and password using Bcrypt
      if user:    
         # Login and validate the user
         login_user(user)
         # check if the url is safe for redirects
         # next = flask.request.args.get('next')
         # if not is_safe_url(next):
         #    return flask.abort(400)

         session["current_user"] = user.username

         return redirect('/user/profile')
      else: 
         flash('Login unsuccessful, please resubmit. If you do not already\
            have an account please register to join.', 'warning')
         
   return redirect('/')

# route for user boards - verify with login_required
@app.route("/user/profile")
# @login_required
def show_user():
   
   user = current_user
   
   """Render user information and hompage boards"""
   # TODO: login_manager.login_message = "Please login"
   board = 'board'
   # TODO: image_urls from API

   image_urls = search('"data_source="American Art&painting"', 9)
   
   return render_template('user/profile.html', image_urls=image_urls, user=user)


@app.route("/user/likes")
# @login_required
def show_likes():
   """Render user likes."""
   login_manager.login_message = "Please login"
   
   return render_template('user/likes.html')
 
 
@app.route("/user/following")
# @login_required
def show_following():
   """Render user following."""
   login_manager.login_message = "Please login"
   
   return render_template('user/following.html')
 

@app.route("/user/logout", methods=['GET','POST'])
# @login_required
def logout():
   '''Logout user.'''
   logout_user()
# TODO:   return render_template('user/logout.html')
   return redirect('/')
if __name__ == "__main__":
     app.run(debug=True)
