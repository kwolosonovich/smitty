# // wasn't able to access/import app.config['SECRET_KEY'] into simthsonian_api to replace "dev" variable
import requests

from flask import Flask, flash, redirect, request, session, url_for, g, Markup, jsonify, render_template
from flask_bootstrap import Bootstrap
from sqlalchemy.exc import IntegrityError

from secure import secret_key, api_key
from smithsonian_api import search, format_images, ApiImage, get_liked_image
from models import db, connect_db, User, Image, Like
from user_form import LoginForm, RegisterForm
from flask_wtf import FlaskForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///smitty"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["CACHE_TYPE"] = "null"
app.config['SECRET_KEY'] = secret_key


connect_db(app)
Bootstrap(app)

db.drop_all()
db.create_all()

CURR_USER = "curr_user"


@app.before_request
def add_user_to_g():
    '''Set G to user.id.'''
    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])
    else:
        g.user = None


def user_login(user):
    '''User login.'''

    session[CURR_USER] = user.id


def user_logout():
    '''User logout.'''
    if CURR_USER in session:
        del session[CURR_USER]


@app.route('/')
def homepage():

    formatted_images = search(search_terms=None, dev=True,
                              images_per_row=9, max_rows=1, max_results=9, is_homepage=True)

    return render_template('homepage.html', formatted_images=formatted_images)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username=username, password=password)
        if user:
            user_login(user)
            return redirect(f'/user/{user.id}/profile')
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    try:
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = User.create(username=username,
                               email=email, password=password)
            db.session.commit()
            user_login(user)
            return redirect(f'/user/{user.id}/profile')
        else:
            return render_template('register.html', form=form)
    except IntegrityError as e:
        flash('Sorry that username is already taken. Please enter a new username')
        return render_template("register.html", form=form)


@app.route("/user/<user_id>/profile")
def show_user(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('user/profile.html', user=user)


@app.route('/user/<user_id>/search', methods=["GET", "POST"])
def search_results(user_id):
    '''Render search results.'''

    if not g.user:
       flash("Please login", "danger")
       return redirect("/login")

    user = User.query.get_or_404(user_id)

    keyword = request.form.get('keyword')
    formatted_images = search(
        search_terms=keyword, max_results=12, dev=True, images_per_row=6, max_rows=2)

    return render_template('user/search.html', formatted_images=formatted_images, user=user)


@app.route('/user/<search_image_id>/like', methods=["GET", "POST"])
def add_like(search_image_id):
    '''Add liked image to database.'''

    if not g.user:
       flash("Please login", "danger")
       return redirect("/login")

    # image = request.form.get('index')
    # image = image.split(", ")
    # # split string into elements
    # url = image[0]
    # title = image[1]
    # artist = image[2]
    # date = image[3]
    # collection = image[4]

    # image_id = request.form.get('index')

    # get liked image data from smithsonian API using the image id
    liked_image = get_liked_image(search_image_id)
    

    if liked_image == None:
        flash('Sorry an error has occured - please relike image')

    # query the Image table for the image
    # image = Image.query.get_or_404(search_image_id)

    else:
        # add the image values and update the image in the Image table
        # image.url = liked_image.url
        # image.title = liked_image.title
        # image.artists = liked_image.artist
        # image.data = liked_image.data
        # image.collection = liked_image.collection

        # save updated image to Image table
        # db.session.commit()

        # add user like to database
        g.user.likes.append(liked_image)
        db.session.commit()

    return redirect(f'/user/{g.user.id}/likes')


@app.route('/user/<user_id>/likes')
def get_likes(user_id):
   '''Get user likes.'''

   if not g.user:
       flash("Please login", "danger")
       return redirect("/login")

   user = User.query.get_or_404(user_id)
   user_likes = user.likes
   formatted_likes = []

   for image in user_likes:
       formatted_img = {
           'url': user.likes[0].url,
           'title': user.likes[0].title,
           'artist': user.likes[0].artist,
           'date': user.likes[0].date,
           'collection': user.likes[0].collection,
           'id': user.likes[0].id
       }
       formatted_likes.append(formatted_img)

   return render_template('user/likes.html', formatted_images=formatted_likes, user=user)


@app.route('/user/<like_id>/unlike', methods=["POST"])
def unlike(like_id):
    '''Remove liked image.'''
    image = Image.query.get_or_404(like_id)

    db.session.delete(image)

    return redirect(f'/user/{g.user.id}/likes')


@app.route("/logout")
def logout():
    '''Logout user.'''

    user_logout()
    flash('Logout successful', 'success')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
