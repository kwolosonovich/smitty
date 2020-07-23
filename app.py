import requests
import pprint

from flask import Flask, render_template, request, flash, redirect, session, g, abort, url_for
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin


from user_form import LoginForm, RegisterForm
from secure import api_key, secret_key
from models import User, connect_db, db, Board, Image, Like, Follow, Like
from seed import seed_database

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///smithsonian'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY']= secret_key

toolbar = DebugToolbarExtension(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)
connect_db(app)

DEBUG = False

if DEBUG:
   seed_database()
else:
   db.create_all()

API_BASE_URL = 'https://api.si.edu/openaccess/api/v1.0/search'


# TODO: Disabling Session Cookie for API


@app.route('/')
def homepage():
   '''Render homepage'''

   # test API requests
   q = "edward hopper"
   rows_ = 1

   # search for items
   resp = requests.get(url=API_BASE_URL,
                       params={"q": q,
                               "api_key": api_key,
                               "rows": rows_})

   # iterate through the items for image URL
   rows = resp.json()["response"]["rows"]
   image_urls = []
   for row in rows:
      if "online_media" in row["content"]["descriptiveNonRepeating"].keys():
         if "resources" in row["content"]["descriptiveNonRepeating"]["online_media"]["media"][0].keys():
            url = row["content"]["descriptiveNonRepeating"]["online_media"]["media"][0]["resources"][0]["url"]
            image_urls.append(url)
      # if "online_media" in row["content"]["descriptiveNonRepeating"].keys():
      #    link = row["content"]["descriptiveNonRepeating"]["online_media"][
      #          "media"][0]["content"]
      #    image_links.append(link)

   print(resp)
   print(len(image_urls))

   return render_template('homepage.html', image_urls=image_urls)


# ********* USER ROUTES *********

# login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
   '''Register new user'''
   
   form = RegisterForm()
   
   if form.validate_on_submit():
      username=form.username.data
      email=form.email.data
      profile_image=form.profile_image.data
      backdrop_image=form.backdrop_image.data
      password=form.password.data

      user = User.create(username, email, profile_image, backdrop_image, password)

      db.session.commit()
         
      redirect_url = url_for('show_boards')
      return redirect(redirect_url)
   
   return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
   '''Login returning user'''
   # TODO: validate if user is already authenticated
   # if current_user.is_authenticated:
   #     return redirect(url_for('show_boards'))
   
   form = LoginForm()
   
   if form.validate_on_submit():
      
      user = User.query.filter_by(username=form.username.data).first()
      if user and authenticate(user.username, form.password.data): 
         login_user(user, remember=form.remember.data, authenticated=True)

      return redirect(url_for('show_boards'))
   
   return render_template('login.html', form=form)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#    # validate if user is already authenticated
#    if current_user.is_authenticated:
#        return redirect(url_for('index'))
#     # Here we use a class of some kind to represent and validate our client-side form data. 
#     # For example, WTForms is a library that will handle this for us, and we use a custom LoginForm to validate.
#     form = LoginForm()
    
#     if form.validate_on_submit():
#         # Login and validate the user.
        
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return('/')
#         # user should be an instance of your `User` class
#         User.login_user(user)

#         flask.flash('Logged in successfully.')

#         next = flask.request.args.get('next')
#         # is_safe_url should check if the url is safe for redirects.
#         # See http://flask.pocoo.org/snippets/62/ for an example.
#         if not is_safe_url(next):
#             return flask.abort(400)

#         return flask.redirect(next or flask.url_for('index'))
#     return flask.render_template('login.html', form=form)


# add route for user boards - requires login_required decorater 
@app.route("/user/boards")
# @login_required
def show_boards():
    return render_template('user/boards.html')


register
@app.route("/user/logout")
# @login_required
def logout():
   '''Logout user'''
   logout_user()
   return render_template('user/logout.html')

if __name__ == "__main__":
     app.run(debug=True)
