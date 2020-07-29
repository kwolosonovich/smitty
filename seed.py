from models import db, User

def seed_database():
    db.rollback()
    db.drop_all()
    db.create_all()

    test_user = User(
        username="Ava",
        email="ava@gmail.com", 
        password="password",
        profile_image='https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=703&q=80', 
        backdrop_image='https://images.unsplash.com/photo-1444927714506-8492d94b4e3d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1355&q=80'
    )
    
    db.session.add(test_user)
    db.session.commit()
    
    
# code to delete db: 
# SELECT pg_terminate_backend(pg_stat_activity.pid)
# FROM pg_stat_activity
# WHERE pg_stat_activity.datname = 'smithsonian'
# AND pid <> pg_backend_pid()
