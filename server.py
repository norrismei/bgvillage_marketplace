"""Server for Board Game Village Marketplace app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
import model

import crud

from jinja2 import StrictUndefined

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

    game_id_str = request.form.get("game_id")
    game_id = int(game_id_str)

    added_game = crud.create_user_game(1, game_id)

    if added_game:
        return "Game was successfully added"
    else:
        return "A problem has occurred"

@app.route('/api/remove-game', methods=['POST'])
def change_own_to_false():
    """Changes own Boolean to false on UserGames table"""

    user_game_id_str = request.form.get("user_game_id")
    user_game_id = int(user_game_id_str)

    removed_game = crud.update_user_game_to_false(user_game_id)

    if removed_game:
        return "Game was successfully removed"
    else:
        return "A problem has occurred"


@app.route('/api/games.json')
def return_all_games():
    """Return all games from database"""

    all_games = model.db.session.query(model.Game).all()

    results = []

    for game in all_games:
        primary_publisher = model.db.session.query(model.GamePublisher).join(
              model.Publisher).filter(model.GamePublisher.game_id == 
              game.id).first()

        results.append(
            {
            "key": game.id,
            "name": game.name,
            "min_players": game.min_players,
            "max_players": game.max_players,
            "publisher": primary_publisher.pub.name,
            "image_url": game.image_url
            })

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