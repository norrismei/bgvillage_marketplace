"""Server for Board Game Village Marketplace app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
import model

import crud

import helper

from jinja2 import StrictUndefined

import requests

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     """View application's homepage. Catches anything that isn't defined route"""

#     return render_template('root.html')

@app.route('/')
def show_homepage():
    """View homepage"""

    return render_template('homepage.html')

@app.route('/users/<username>')
def show_user_page(username):
    """View user's personal page"""

    return render_template('user_page.html', username=username)

@app.route('/games')
def show_all_games():
    """View all games from database"""

    return render_template('all_games.html')

@app.route('/api/add-game', methods=['POST'])
def add_game_to_database():
    """Add a UserGame"""

    atlas_id_str = request.form.get("atlas_id")
    atlas_id = int(atlas_id_str)
    add_type = request.form.get("add_type")

    status = add_game_to_database(atlas_id, add_type)

    return status

@app.route('/api/remove-game', methods=['POST'])
def change_own_to_false():
    """Changes own Boolean to false on UserGames table"""

    game_id_str = request.form.get("user_game_id")
    game_id = int(game_id_str)
    remove_type = request.form.get("remove_type")

    removed_game = False
    if remove_type == "own":
        removed_game = crud.update_user_game_to_false(game_id)
    elif remove_type == "wishlist":
        removed_game = crud.delete_wanted_game(game_id)

    if removed_game:
        return "Game was successfully removed"
    else:
        return "A problem has occurred"


@app.route('/api/games.json')
def return_all_games():
    """Return games from database matching search terms"""

    search_terms = request.args.get("search_terms")

    results = helper.search_board_game_atlas(search_terms)

    return jsonify(results)


@app.route('/api/own_games.json')
def show_user_own_games():
    """Return JSON for list of user's owned games"""

    own_games = model.db.session.query(model.UserGame).join(model.User).filter(
                model.User.username=="norrism3", model.UserGame.own==True).all()

    results = []

    for own_game in own_games:
        results.append(
            {
            "key": own_game.id,
            "name": own_game.game.name,
            "min_players": own_game.game.min_players,
            "max_players": own_game.game.max_players,
            "min_playtime": own_game.game.min_playtime,
            "max_playtime": own_game.game.max_playtime,
            "image_url": own_game.game.image_url
            }
        )

    return jsonify(results)


@app.route('/api/listed_games.json')
def show_user_sell_games():
    """Return JSON for list of user's games for sale"""

    listed_games = model.db.session.query(model.ListedGame).select_from(
                 model.ListedGame).join(model.UserGame).join(model.User).join(
                 model.Game).filter(model.User.username=="norrism3").all()

    results = []

    for listed_game in listed_games:
        results.append(
            {
            "key": listed_game.id,
            "name": listed_game.user_game.game.name,
            "condition": listed_game.condition,
            "price": listed_game.price,
            "comment": listed_game.comment,
            "image_url": listed_game.user_game.game.image_url
            }
        )

    return jsonify(results)

@app.route('/api/wanted_games.json')
def show_user_want_games():
    """Return JSON for list of games user wants"""

    wanted_games = model.db.session.query(model.WantedGame).select_from(
                 model.WantedGame).join(model.User).join(model.Game).filter(
                 model.User.username=="norrism3").all()

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

    return jsonify(results)


if __name__ == '__main__':
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)