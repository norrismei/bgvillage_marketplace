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

@app.route('/login')
def show_login():
    """View login page"""

    return render_template('login.html')


@app.route('/handle-login', methods=['POST'])
def handle_login():
    """Log user into site"""

    username = request.form['username']
    password = request.form['password']

    user = crud.lookup_user(username)
    if not user:
        print(f"Reached if not user")
        flash("No account with this username. Please sign up.")
        return redirect('/login')

    if password == crud.get_password(username):
        session['current_user'] = username
        return redirect(f"/users/{username}")
    else:
        flash("Wrong password. Please try again.")
        return redirect('/login')


@app.route('/sign-up')
def show_sign_up():
    """View sign up form"""


    return render_template('signup.html', 
                            email_warning=False,
                            username_warning=False,
                            password_warning=False,
                            email="",
                            username="",
                            fname="",
                            lname="",
                            birthdate="")


@app.route('/process-sign-up', methods=['POST'])
def handle_sign_up():
    """Create new user and redirects to user page"""

    email = request.form.get('email')
    email_warning = helper.check_email(email)

    username = request.form.get('username')
    username_warning = helper.check_username(username)

    password = request.form.get('password')
    repeat_password = request.form.get('repeat-password')
    password_warning = helper.check_if_not_same(password, repeat_password)

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    birthdate = request.form.get('birthdate')

    if email_warning or username_warning or password_warning:
        return render_template('signup.html', 
                                email_warning=email_warning,
                                username_warning=username_warning,
                                password_warning=password_warning,
                                email=email,
                                username=username,
                                fname=fname,
                                lname=lname,
                                birthdate=birthdate)

    crud.create_user(username, fname, lname, email, password, birthdate)
    session['current_user'] = username

    flash(f"Welcome to the Village, {username}")
    return redirect(f'/users/{username}')


@app.route('/logout')
def handle_logout():
    """Logs user out of site"""

    del session['current_user']

    flash("You've successfully logged out.")
    return redirect('/login')


@app.route('/')
def show_homepage():
    """View homepage"""

    if 'current_user' not in session:
        return redirect('/login')
    else:
        username = session['current_user']
        return redirect(f'/users/{username}')

    return render_template('homepage.html')


@app.route('/users/')
def redirect_to_user_page():
    """Redirects to current user's page"""

    if 'current_user' not in session:
        flash('Please log in first')
        return redirect('/login')
    else:
        username = session['current_user']
        return redirect(f'/users/{username}')


@app.route('/users/<username>')
def show_user_page(username):
    """View user's personal page"""

    if 'current_user' not in session:
        flash('Please log in first')
        return redirect('/login')
    else:
        return render_template('user_page.html', username=username)


@app.route('/games')
def show_all_games():
    """View all games from database"""

    if 'current_user' not in session:
        flash('Please log in first')
        return redirect('/login')
    else:
        return render_template('all_games.html')


@app.route('/marketplace')
def show_all_listings():
    """View all games from database"""

    if 'current_user' not in session:
        flash('Please log in first')
        return redirect('/login')
    else:
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

    user_game_id_str = request.form.get("user_game_id")
    user_game_id = int(user_game_id_str)
    remove_type = request.form.get("remove_type")

    status = helper.remove_game(remove_type, user_game_id)

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

    username = session['current_user']

    own_games = helper.get_user_own_games(username)

    return jsonify(own_games)


@app.route('/api/user/own-games/to-sell.json')
def show_available_to_sell():
    """Return JSON for list of user's games available to sell"""

    username = session['current_user']

    able_to_sell = helper.get_user_games_able_to_sell(username)

    return jsonify(able_to_sell)


@app.route('/api/user/listed-games.json')
def show_user_listed_games():
    """Return JSON for list of user's games for sale"""

    username = session['current_user']

    listed_games = helper.get_user_listed_games(username)

    return jsonify(listed_games)


@app.route('/api/marketplace.json')
def get_marketplace_listings():
    """Return JSON for all listings from all users"""

    search_terms = request.args.get("search_terms")
    username = session['current_user']

    listed_games = helper.search_marketplace_listings(
                   search_terms, username)

    return jsonify(listed_games)


@app.route('/api/marketplace/<username>.json')
def filter_listings_by_username(username):
    """Return JSON for all listings filtered by username"""

    # Replace with user in session in the future
    user = session['current_user']
    selected_username = username

    filtered_listings = helper.filter_listings_by_username(
        user, selected_username)

    return jsonify(filtered_listings)


@app.route('/api/listing/details.json')
def get_listing_details():
    """Return JSON for a single listing"""

    listing_id = request.args.get("listing_id") 
    username = request.args.get("username")

    return helper.get_listing_details(listing_id, username)


@app.route('/api/user/email.json')
def lookup_seller_email():
    """Returns a user's email address"""

    username = request.args.get("username")

    return crud.get_email_by_username(username)


@app.route('/api/user/wanted-games.json')
def show_user_want_games():
    """Return JSON for list of games user wants"""

    username = session['current_user']

    wanted_games = helper.get_user_wanted_games(username)

    return jsonify(wanted_games)


if __name__ == '__main__':
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)