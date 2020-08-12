'''SQLAlchemy models'''

from flask import session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    '''Users model.'''

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.String,
        nullable=False,
    )

    likes = db.relationship(
        'Image',
        secondary="likes"
    )

    @classmethod
    def authenticate(cls, username, password):
        """Valid username and password."""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    @classmethod
    def create(cls, username, email, password):
        '''Register a new user and hash password'''

        hashed = bcrypt.generate_password_hash(password)
        hashed_password = hashed.decode("utf8")
        user = cls(
            username=username,
            email=email,
            password=hashed_password,
        )
        db.session.add(user)
        return user


class Image(db.Model):
    '''Images model'''

    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    url = db.Column(
        db.String
    )

    title = db.Column(
        db.String
    )

    artist = db.Column(
        db.String
    )

    date = db.Column(
        db.String
    )

    collection = db.Column(
        db.Text
    )

    search_image_id = db.Column(
        db.Text
    )

    @classmethod
    def add_image(cls, url, title, artist, date, collection, search_image_id):
        image = cls(
            url=url,
            title=title,
            artist=artist,
            date=date,
            collection=collection,
            search_image_id=search_image_id
        )
        db.session.add(image)
        return image

    @classmethod
    def add_search_image(cls, search_image_id):
        image = cls(
            search_image_id=search_image_id
        )
        db.session.add(image)
        return image


class Like(db.Model):
    '''User likes for images model.'''

    __tablename__ = 'likes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id',
                      ondelete='CASCADE'
                      )
    )

    image_id = db.Column(
        db.Integer,
        db.ForeignKey('images.id',
                      #   ondelete='CASCADE'
                      )
    )


def connect_db(app):
    '''Connect database to Flask app.'''

    db.app = app
    db.init_app(app)
