"""Server for Board Game Village Marketplace app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/users/<username>')
def show_user_homepage(username):
    """View homepage"""

    #If not logged in, redirect to login page

    return render_template('user_page.html')


@app.route('/games')
def show_all_games():
    """View search to add games to personal list"""

    return render_template('all_games.html')


@app.route('/marketplace')
def show_game_database():
    """View list of games for sale"""

    return render_template('marketplace.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)