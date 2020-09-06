import requests

import crud

import model

import rec_helper
import format_helper

from flask_sqlalchemy import SQLAlchemy


def get_user_own_games(username):
    """Returns list of user's own games as dictionary, including its sell status"""

    own_games = crud.get_user_current_own_games(username)

    results = []

    for own_game in own_games:
        
        selling = False
        try:
            if own_game.listing.active:
                selling = True
        except:
            pass
        
        results.append(
            {
            "key": own_game.id,
            "name": own_game.game.name,
            "min_players": own_game.game.min_players,
            "max_players": own_game.game.max_players,
            "min_playtime": own_game.game.min_playtime,
            "max_playtime": own_game.game.max_playtime,
            "image_url": own_game.game.image_url,
            "selling": selling
            }
        )

    return results



def get_user_wanted_games(username):
    """Returns list of user's wanted games as dictionary"""

    wanted_games = crud.get_user_wanted_games(username)

    results = []

    for wanted_game in wanted_games:
        results.append(
            {
            "key": wanted_game.id,
            "name": wanted_game.game.name,
            "min_players": wanted_game.game.min_players,
            "max_players": wanted_game.game.max_players,
            "min_playtime": wanted_game.game.min_playtime,
            "max_players": wanted_game.game.max_players,
            "image_url": wanted_game.game.image_url
            }
        )

    return results


def remove_game(remove_type, user_game_id):
    """Updates UserGame to own=False or deletes WantedGame"""

    removed_game = False
    if remove_type == "own":
        deactivated = crud.update_listed_game_to_false(user_game_id)
        removed_game = crud.update_user_game_to_false(user_game_id)
    elif remove_type == "wishlist":
        removed_game = crud.delete_wanted_game(user_game_id)

    if removed_game:
        return "Game was successfully removed"
    else:
        return "A problem has occurred"


def get_id_set(games):
    """Takes in list of game objects. Returns set of ids"""

    id_set = set([])
    for game in games:
        id_set.add(game.game_id)

    return id_set


def get_game_set(games):
    """Takes in list of UserGames or WantedGames and returns Games set"""

    game_set = set([])
    for game in games:
        game_set.add(game.game)

    return game_set


def get_game_details(id):
    """Takes in UserGame id and returns basic game details"""

    user_game = crud.get_user_game_by_id(id)
    game = user_game.game

    (image_url, game_name, min_age, publish_year, 
    description, players, playtime, msrp, primary_publisher, 
    designers, mechanics, categories) = format_helper.format_game_details(game)

    return {
        "key": user_game.id,
        "image_url": image_url,
        "game_name": game_name,
        "msrp": msrp,
        "min_age": min_age,
        "players": players,
        "playtime": playtime,
        "publisher": primary_publisher,
        "designers": designers,
        "publish_year": publish_year,
        "game_description": description,
        "mechanics": mechanics,
        "categories": categories,
    }
    

if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)

