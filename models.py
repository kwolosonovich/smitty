'''SQLAlchemy models'''

from flask import session
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()
# login_manager = LoginManager()

    
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
    #                          backref="user", 
    #                          cascade="all, delete")
    
    boards = db.relationship("Board",
                             backref=db.backref('user'),
                             cascade='all, delete-orphan' 
                             )
    
    # like_image = db.relationship("Like",
    #                         backref=db.backref('user')
    #                         )
    
    
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


    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated


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
        
        if bcrypt.check_password_hash(user.password, password):
            return True
        else:
            return False
    
    
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

    #TODO: remove class if db.Table below continues to work
# class Board_Images(db.Model):
#     __tablename__ = 'board_images'
    
#     board_id = db.Column(db.Integer,
#                          db.ForeignKey('boards.id', ondelete="cascade"),
#                          primary_key=True)
 
#     images_id = db.Column(db.Integer,
#                          db.ForeignKey('images.id', ondelete="cascade"),
#                          primary_key=True)
    
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
    # login_manager.init_app(app)
#     # login_manager(app)
