"""CRUD operations"""

from model import db, User, Game, Mechanic, GameMechanic, connect_to_db


def create_user(username, fname, lname, email, password, birthdate=None):
    """Create and return a new user"""

    user = User(username=username, fname=fname, lname=lname,
                email=email, password=password, birthdate=birthdate)

    db.session.add(user)
    db.session.commit()

    return user


def create_game(name, description=None, publish_year=None, min_age=None,
                min_players=None, max_players=None, 
                min_playtime=None, max_playtime=None,
                image_url=None, msrp=None):
    """Create and return a new game"""

    game = Game(name=name, description=description, publish_year=publish_year, 
                min_age=min_age, min_players=min_players, 
                max_players=max_players, min_playtime=min_playtime, 
                max_playtime=max_playtime, image_url=image_url, msrp=msrp)

    db.session.add(game)
    db.session.commit()

    return game


def create_mechanic(name, atlas_id=None):
    """Create and return a new gaming mechanic"""

    mechanic = Mechanic(name=name, atlas_id=atlas_id)

    db.session.add(mechanic)
    db.session.commit()


def create_game_mechanic(game_id, mechanic_id):
    """Create and return a new game tagged with mechanic instance"""

    game_mechanic = GameMechanic(game_id=game_id, mechanic_id=mechanic_id)

    db.session.add(game_mechanic)
    db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)