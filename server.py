"""Server for Board Game Village Marketplace app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
import model

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """View application's homepage. Catches anything that isn't defined route"""

    return render_template('root.html')


@app.route('/api/own_games.json')
def show_user_own_games():
    """Return JSON for list of user's owned games"""

    own_games = model.db.session.query(model.UserGame).join(model.User).filter(
                model.User.username=="norrism3").all()

    results = []

    for own_game in own_games:
        results.append(
            {
            "key": own_game.id,
            "name": own_game.game.name
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
            "name": listed_game.user_game.game.name
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
            "name": wanted_game.game.name
            }
        )

    return jsonify(results)


if __name__ == '__main__':
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)