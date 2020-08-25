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


def get_email_by_username(username):
    """Takes in username and returns email of matching user"""

    user = User.query.filter_by(username=username).one()

    return user.email


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


def get_game_by_name(name):
    """Takes in string and finds match with Game in db, if any"""

    existing_game = db.session.query(Game).filter_by(name=name).first()

    if existing_game:
        return existing_game
    else:
        return None


def get_game_by_atlas_id(atlas_id):
    """Takes in atlas_id and returns matching Game, if any"""

    existing_game = db.session.query(Game).filter_by(atlas_id=atlas_id).first()

    if existing_game:
        return existing_game
    else:
        return None



def create_user_game(user_id, game_id, own=True):
    """Create and return an instance of game owned by user"""

    user_game = UserGame(user_id=user_id, game_id=game_id, own=own)

    db.session.add(user_game)
    db.session.commit()

    return user_game


def get_user_own_games(username):
    """Takes in username and returns user's UserGames"""

    own_games = db.session.query(UserGame).join(User).filter(
                User.username==username, UserGame.own==True).all()

    return own_games


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


def get_user_listed_games(username):
    """Takes in a username and returns user's listed games"""

    listed_games = db.session.query(ListedGame).select_from(
                   ListedGame).join(UserGame).join(User).join(
                   Game).filter(User.username==username).all()

    # listed_games = db.session.query(ListedGame).select_from(ListedGame).join(
    #                User).filter(User.username==username).all()

    return listed_games


def get_marketplace_listings(search_terms):
    """Returns all ListedGames from all Users"""

    listed_games = db.session.query(ListedGame).select_from(ListedGame).join(
                   UserGame).join(Game).filter(
                   Game.name.ilike(f'%{search_terms}%')).all()

    return listed_games


def get_listing_details(listing_id):
    """Takes in listing ID and returns game listing details"""

    listed_game = db.session.query(ListedGame).filter_by(id=listing_id).one()

    return listed_game


def delete_listed_game(id):
    """Finds ListedGame by id and removes row"""

    listed_game = ListedGame.query.get(id)

    db.session.delete(listed_game)
    db.session.commit()


def get_listed_game_by_id(user_game_id):
    """Takes in a UserGame id and returns a matching ListedGame, if any"""

    listed_game = db.session.query(ListedGame).filter_by(id=user_game_id).first()

    if listed_game:
        return listed_game
    else:
        return None


def create_wanted_game(user_id, game_id):
    """Create and return an instance of game wanted by user"""

    wanted_game = WantedGame(user_id=user_id, game_id=game_id)

    db.session.add(wanted_game)
    db.session.commit()

    return wanted_game


def get_user_wanted_games(username):
    """Takes in username and returns user's WantedGames"""

    wanted_games = db.session.query(WantedGame).select_from(WantedGame).join(
                   User).join(Game).filter(User.username==username).all()

    return wanted_games

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