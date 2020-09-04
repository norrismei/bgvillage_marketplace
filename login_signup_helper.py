import crud

import model

from flask_sqlalchemy import SQLAlchemy


def check_email(email):
    """Checks if email address is already in database"""

    existing_email = crud.lookup_email(email)

    if existing_email:
        return True
    else:
        return False


def check_username(username):
    """Checks if username already exists in database"""

    existing_username = crud.lookup_user(username)

    if existing_username:
        return True
    else:
        return False


def check_if_not_same(value1, value2):
    """Checks if two entered values are not the same"""

    if value1 == value2:
        return False
    else:
        return True


if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)