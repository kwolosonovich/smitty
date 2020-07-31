from werkzeug.security import generate_password_hash
from models import db, User
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


def seed_database():
    db.session.rollback()
    db.drop_all()
    db.create_all()
    
    password = b'margs_utf8'
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    test_user = User(
        username="Margaux",
        email="margaux@gmail.com", 
        password=hashed_password,
    )
    
    db.session.add(test_user)
    db.session.commit()
    
    
# code to delete db: 
# SELECT pg_terminate_backend(pg_stat_activity.pid)
# FROM pg_stat_activity
# WHERE pg_stat_activity.datname = 'smithsonian'
# AND pid <> pg_backend_pid()
