'''SQLAlchemy models'''

from flask import session
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_manager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
    
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
    
    authenticated = db.Column(
        db.Boolean, 
        nullable=False,
        default=False
    )
    
    # boards = db.relationship("Board", 
    #                          backref=db.backref('user',
    #                          cascade="all, delete-orphan"
    #                          ))
    
    boards = db.relationship("Board",
                             backref=db.backref('user'),
                             cascade='all, delete-orphan' 
                             )
 
    # likes = db.relationship("Like",
    #                         backref=db.backref('user',
    #                         cascade="all, delete-orphan"
    #                         ))
    
    likes = db.relationship("Like",
                            backref=db.backref('user'))
    
    # @login.user_loader
    # def load_user(user_id):
    #     '''Load a user'''
    #     return User.query.get(user_id
    
    # @classmethod
    # def login_user(self, remember=False, duration=None, force=False, fresh=True):
    #     '''Login user'''
    #     user_id = getattr(user, current_app.login_manager.id_attribute)()
    #     session['user_id'] = user_id
    #     session['_fresh'] = fresh
    #     session['_id'] = current_app.login_manager._session_identifier_generator()
    
    #     current_app.login_manager._update_request_context_with_user(user)
    #     user_logged_in.send(current_app._get_current_object(), user=_get_user())      
    #     return True
    
    # @classmethod
    # def login_fresh():
    #     ''' This returns ``True`` if the current login is fresh.'''
    #     return session.get('_fresh', False)
    
    # def is_active(self):
    #     """True, as all users are active."""
    #     return True

    # def get_id(self):
    #     """Return the email address to satisfy Flask-Login's requirements."""
    #     return self.email

    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated

    # def is_anonymous(self):
    #     """False, as anonymous users aren't supported."""
    #     return False

    
class Board(db.Model):
    '''User board model.'''

    __tablename__= 'boards'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        cascade='all, delete-orphan'
    )
    
    user_id = db.Column(
        db.Integer,
        # db.ForeignKey('users.id', cascade="all, delete-orphan")
        db.ForeignKey('users.id')
    )
    
    name = db.Column(
        db.String
    )
    
    board_images = db.relationship('board_images',
                                   backref=db.backref('board'))
    
    
class Image(db.Model):
    '''Images model'''

    __tablename__= 'images'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
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
    '''User likes model.'''

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


'''Boards and images table'''
board_images = db.Table('board_images', 
                        db.Column('board_id', 
                                  db.Integer, 
                                  db.ForeignKey('boards.id'), 
                                  primary_key=True),
                        db.Column('image.id',
                                db.Integer,
                                db.ForeignKey('images.id'),
                                primary_key=True)
                        )
                            

def connect_db(app):
    '''Connect database to Flask app.'''

    db.app = app
    db.init_app(app)
#     # Initialize login plugin
#     # login_manager.init_app(app)
#     # login_manager(app)
