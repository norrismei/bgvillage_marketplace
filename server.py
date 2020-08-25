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


@app.route('/marketplace')
def show_all_listings():
    """View all games from database"""

    return render_template('marketplace.html')


@app.route('/api/add-game', methods=['POST'])
def add_game_to_database():
    """Add a UserGame"""

    add_type = request.form.get("add_type")
    name = request.form.get("name")
    atlas_id = request.form.get("atlas_id")

    if atlas_id:
        status = helper.add_game_to_database(add_type, name, atlas_id)
    else:
        status = helper.add_game_to_database(add_type, name)

    return status


@app.route('/api/list-game', methods=['POST'])
def list_game():

    user_game_id = request.form.get("game")
    condition = request.form.get("condition")
    price = float(request.form.get("price"))
    comment = request.form.get("comment")

    listed_game = crud.create_listed_game(user_game_id, condition, price, comment)

    return "Game was successfully listed"


@app.route('/api/remove-game', methods=['POST'])
def remove_game():
    """Changes own Boolean to false on UserGames table"""

    game_id_str = request.form.get("user_game_id")
    game_id = int(game_id_str)
    remove_type = request.form.get("remove_type")

    status = helper.remove_game(remove_type, game_id)

    return status


@app.route('/api/games/search.json')
def search_atlas_games():
    """Return games from Board Game Atlas matching search terms"""

    search_terms = request.args.get("search_terms")

    results = helper.search_board_game_atlas(search_terms)

    return jsonify(results)


@app.route('/api/user/own-games.json')
def show_user_own_games():
    """Return JSON for list of user's owned games"""

    own_games = helper.get_user_own_games(username="norrism3")

    return jsonify(own_games)


@app.route('/api/user/own-games/to-sell.json')
def show_available_to_sell():
    """Return JSON for list of user's games available to sell"""

    able_to_sell = helper.get_user_games_able_to_sell(username="norrism3")

    return jsonify(able_to_sell)


@app.route('/api/user/listed-games.json')
def show_user_listed_games():
    """Return JSON for list of user's games for sale"""

    listed_games = helper.get_user_listed_games(username="norrism3")

    return jsonify(listed_games)


@app.route('/api/marketplace.json')
def get_marketplace_listings():
    """Return JSON for all listings from all users"""

    search_terms = request.args.get("search_terms")

    listed_games = helper.search_marketplace_listings(search_terms)

    return jsonify(listed_games)


@app.route('/api/marketplace/wishlist-filter.json')
def filter_listings_by_wishlist():
    """Return JSON for all listings filtered by user's wishlist"""

    filtered_listings = helper.filter_listings_by_wishlist(username="norrism3")

    return jsonify(filtered_listings)


@app.route('/api/listing/details.json')
def get_listing_details():
    """Return JSON for a single listing"""

    listing_id = request.args.get("listing_id") 

    return helper.get_listing_details(listing_id)


@app.route('/api/user/email.json')
def lookup_seller_email():
    """Returns a user's email address"""

    username = request.args.get("username")

    return crud.get_email_by_username(username)


@app.route('/api/user/wanted-games.json')
def show_user_want_games():
    """Return JSON for list of games user wants"""

    wanted_games = helper.get_user_wanted_games(username="norrism3")

    return jsonify(wanted_games)


if __name__ == '__main__':
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)