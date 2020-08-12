"""CRUD operations"""

from model import db, User, connect_to_db

def create_user(username, fname, lname, email, password, birthdate=None):
    """Create and return a new user."""

    user = User(username=username, fname=fname, lname=lname,
                email=email, password=password, birthdate=birthdate)

    db.session.add(user)
    db.session.commit()

    return user

if __name__ == '__main__':
    from server import app
    connect_to_db(app)