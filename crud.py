"""CRUD operations"""

from model import (db, User, Game, UserGame, Mechanic, GameMechanic, Category,
                   GameCategory, Publisher, GamePublisher, Designer,
                   GameDesigner, Artist, GameArtist, connect_to_db)


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


def create_user_game(user_id, game_id, own=True):
    """Create and return an instance of game owned by user"""

    user_game = UserGame(user_id=user_id, game_id=game_id, own=own)

    db.session.add(user_game)
    db.session.commit()

    return user_game


def create_mechanic(name, atlas_id=None):
    """Create and return a new gaming mechanic"""

    mechanic = Mechanic(name=name, atlas_id=atlas_id)

    db.session.add(mechanic)
    db.session.commit()

    return mechanic


def create_game_mechanic(game_id, mechanic_id):
    """Create and return a new game tagged with mechanic instance"""

    game_mechanic = GameMechanic(game_id=game_id, mechanic_id=mechanic_id)

    db.session.add(game_mechanic)
    db.session.commit()

    return game_mechanic


def create_category(name, atlas_id=None):
    """Create and return a new gaming category"""

    category = Category(name=name, atlas_id=atlas_id)

    db.session.add(category)
    db.session.commit()

    return category


def create_game_category(game_id, category_id):
    """Create and return a new game tagged with category instance"""

    game_category = GameCategory(game_id=game_id, category_id=category_id)

    db.session.add(game_category)
    db.session.commit()

    return game_category


def create_publisher(name):
    """Create and return a new gaming category"""

    publisher = Publisher(name=name)

    db.session.add(publisher)
    db.session.commit()

    return publisher


def create_game_publisher(game_id, publisher_id):
    """Create and return a new game tagged with publisher instance"""

    game_publisher = GamePublisher(game_id=game_id, publisher_id=publisher_id)

    db.session.add(game_publisher)
    db.session.commit()

    return game_publisher


def create_designer(name):
    """Create and return a new game designer"""

    designer = Designer(name=name)

    db.session.add(designer)
    db.session.commit()

    return designer


def create_game_designer(game_id, designer_id):
    """Create and return a new game tagged with designer instance"""

    game_designer = GameDesigner(game_id=game_id, designer_id=designer_id)

    db.session.add(game_designer)
    db.session.commit()

    return game_designer


def create_artist(name):
    """Create and return a new game artist"""

    artist = Artist(name=name)

    db.session.add(artist)
    db.session.commit()

    return artist


def create_game_artist(game_id, artist_id):
    """Create and return a new game tagged with artist instance"""

    game_artist = GameArtist(game_id=game_id, artist_id=artist_id)

    db.session.add(game_artist)
    db.session.commit()

    return game_artist


if __name__ == '__main__':
    from server import app
    connect_to_db(app)