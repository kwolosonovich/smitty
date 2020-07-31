'''SQLAlchemy models'''

from flask import session
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()

login_manager = LoginManager()

class User(UserMixin, db.Model):
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
    
    profile_image = db.Column(
        db.String,
        nullable=True
    )

    backdrop_image = db.Column(
        db.String,
        nullable=True,
    )
    
    password = db.Column(
        db.String,
        nullable=False,
    )
    
    # boards = db.relationship("Board",
    #                          backref="user", 
    #                          cascade="all, delete")
    
    boards = db.relationship("Board",
                             backref=db.backref('user'),
                             cascade='all, delete-orphan' 
                             )
    
    # like_image = db.relationship("Like",
    #                         backref=db.backref('user')

    @login_manager.user_loader
    def load_user(user_id):
        """Check if user is logged-in on every page load."""
        return User.query.get(int(user_id))


    @classmethod
    def create(cls, username, email, profile_image, backdrop_image, password):
        '''Register a new user and hash password'''
        
        # hash password
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        
        user = cls(
            username=username,
            email=email,
            profile_image=profile_image,
            backdrop_image=backdrop_image,
            password=hashed_utf8,
        )
        # add user to session
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Valid username and password."""
        
        user = cls.query.filter_by(username=username).first()
        
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    # def user_login(user):
    #     """Log in user."""
    #     session[CURR_USER_KEY] = user.id

    @classmethod
    def verify_login(user=None):
        """Validate if user is logged in."""

        if 'CURR_USER_KEY' in session and 'CURR_USER_KEY' == User.query.get('CURR_USER_KEY'):
            user = User.query.get(session[CURR_USER_KEY])
            return user
        else: 
            return None

class Board(db.Model):
    '''User board model.'''

    __tablename__= 'boards'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        # cascade='all, delete-orphan'
    )
    
    user_id = db.Column(
        db.Integer,
        # db.ForeignKey('users.id', cascade="all, delete-orphan")
        db.ForeignKey('users.id')
    )
    
    name = db.Column(
        db.String
    )
    # TODO: revisit to find out why it causes a mapper error
    # board_images = db.relationship('board_images',
    #                                backref=db.backref('board'))
    
    
class Image(db.Model):
    '''Images model'''

    __tablename__= 'images'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    # image_path = db.Column(
    #     db.String
    # )
    
    title = db.Column(
        db.String 
    )
    
    description = db.Column (
        db.Text
    )
    
    published = db.Column(
        db.String
    )


class Like(db.Model):
    '''User likes for images model.'''

    __tablename__ = 'likes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        # db.ForeignKey('users.id', cascade="all, delete-orphan"),
        db.ForeignKey('users.id', 
                    #   ondelete='CASCADE'
                      )
    )

    image_id = db.Column(
        db.Integer,
        db.ForeignKey('images.id' 
                    #   ondelete='CASCADE'
                      )
    )
    

class Follow(db.Model):
    '''User following boards model.'''

    __tablename__ = 'follows'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        # db.ForeignKey('users.id', cascade="all, delete-orphan"),
        db.ForeignKey('users.id',
                      #   ondelete='CASCADE'
                      )
    )

    board_id = db.Column(
        db.Integer,
        db.ForeignKey('images.id'
                      #   ondelete='CASCADE'
                      )
    )
    
'''Boards and images table'''
board_images = db.Table('board_images', 
                        db.Column('boards.id', 
                                  db.Integer, 
                                  db.ForeignKey('boards.id'), 
                                  primary_key=True),
                        db.Column('images.id',
                                db.Integer,
                                db.ForeignKey('images.id'),
                                primary_key=True)
                        )
 


def connect_db(app):
    '''Connect database to Flask app.'''

    db.app = app
    db.init_app(app)
#     # Initialize login plugin
    login_manager.init_app(app)
#     # login_manager(app)

