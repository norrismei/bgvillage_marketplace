"""CRUD operations"""

from model import (db, User, Game, UserGame, ListedGame, WantedGame, 
                   Mechanic, GameMechanic, Category, GameCategory, Publisher, 
                   GamePublisher, Designer, GameDesigner, Artist, GameArtist, 
                   connect_to_db)


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
                image_url=None, msrp=None, atlas_id=None):
    """Create and return a new game"""

    game = Game(name=name, description=description, publish_year=publish_year, 
                min_age=min_age, min_players=min_players, 
                max_players=max_players, min_playtime=min_playtime, 
                max_playtime=max_playtime, image_url=image_url, msrp=msrp,
                atlas_id=atlas_id)

    db.session.add(game)
    db.session.commit()

    return game


def get_game_id_by_atlas_id(atlas_id):
    """Takes in atlas_id and returns id of matching Game"""

    return "hi"



def create_user_game(user_id, game_id, own=True):
    """Create and return an instance of game owned by user"""

    user_game = UserGame(user_id=user_id, game_id=game_id, own=own)

    db.session.add(user_game)
    db.session.commit()

    return user_game


def update_user_game_to_false(id):
    """Finds UserGame by id and updates Own boolean to false"""

    user_game = UserGame.query.get(id)
    user_game.own = False
    db.session.commit()

    return user_game


def delete_wanted_game(id):
    """Finds WantedGame by id and removes row"""

    wanted_game = WantedGame.query.get(id)
    db.session.delete(wanted_game)
    db.session.commit()


def create_listed_game(user_games_id, condition, price, comment=None):
    """Takes ID of existing UserGame object and creates ListedGame object"""

    listed_game = ListedGame(id=user_games_id, condition=condition,
                             price=price, comment=comment)

    db.session.add(listed_game)
    db.session.commit()

    return listed_game


def create_wanted_game(user_id, game_id):
    """Create and return an instance of game wanted by user"""

    wanted_game = WantedGame(user_id=user_id, game_id=game_id)

    db.session.add(wanted_game)
    db.session.commit()

    return wanted_game

#####Removed Rating component####
# def create_rating(user_id, game_id, rating, comment=None):
#     """Create and return a game rating"""

#     rating = Rating(user_id=user_id, game_id=game_id,
#                     rating=rating, comment=comment)

#     db.session.add(rating)
#     db.session.commit()

#     return rating


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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)