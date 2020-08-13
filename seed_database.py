"""Script to seed database"""

import os
import json
from random import choice
from datetime import datetime

import crud
import model
import server

from flask_sqlalchemy import SQLAlchemy

os.system('dropdb bgvillage')
os.system('createdb bgvillage')

model.connect_to_db(server.app)
model.db.create_all()

# Create empty list to hold new user objects
users_list = []
with open('data/users.json') as f:
    user_data = json.loads(f.read())

    for user in user_data:
        username = user["username"]
        fname = user["fname"]
        lname = user["lname"]
        email = user["email"]
        password = user["password"]
        
        birthdate_str = user["birthdate"]
        birthdate_format = "%b %d, %Y"
        birthdate = datetime.strptime(birthdate_str, birthdate_format)

        new_user = crud.create_user(username, fname, lname, email, 
                                    password, birthdate)
        users_list.append(new_user)

with open('data/mechanics.json') as f:
    mechanic_data = json.loads(f.read())

    for mechanic in mechanic_data:
        name = mechanic["name"]
        atlas_id = mechanic["id"]

        crud.create_mechanic(name, atlas_id)

with open('data/categories.json') as f:
    category_data = json.loads(f.read())

    for category in category_data:
        name = category["name"]
        atlas_id = category["id"]

        crud.create_category(name, atlas_id)

# Create empty list to hold new game objects
games_list = []
with open('data/games.json') as f:
    game_data = json.loads(f.read())

    for game in game_data:
        name = game["name"]
        description = game["description"]
        publish_year = game["year_published"]
        min_age = game["min_age"]
        min_players = game["min_players"]
        max_players = game["max_players"]
        min_playtime = game["min_playtime"]
        max_playtime = game["max_playtime"]
        image_url = game["image_url"]
        msrp = float(game["msrp"])

        new_game = crud.create_game(name, description, publish_year, min_age,
                        min_players, max_players, min_playtime, max_playtime,
                        image_url, msrp) 
        games_list.append(new_game)

        # Create GameMechanic objects for game's mechanics
        # Get a list of dictionaries containing mechanic atlas_id's
        mechanics_list = game["mechanics"]

        # Iterate through the list, as long as it's not empty
        if len(mechanics_list) > 0:
            for mechanic in mechanics_list:
                atlas_id = mechanic["id"]
                # Try to match the atlas_id with what's in db to get mech id.
                # If can't find a match, skip it.
                try:
                    mech = model.db.session.query(model.Mechanic).filter_by(
                           atlas_id = atlas_id).first()
                    crud.create_game_mechanic(new_game.id, mech.id)
                except:
                    continue

        # Create GameCategory objects for game's categories
        # Get a list of dictionaries containing category atlas_id's
        categories_list = game["categories"]

        # Iterate through the list, as long as it's not empty
        if len(categories_list) > 0:
            for category in categories_list:
                atlas_id = category["id"]
                # Try to match the atlas_id with what's in db to get cat id.
                # If can't find a match, skip it.
                try:
                    cat = model.db.session.query(model.Category).filter_by(
                           atlas_id = atlas_id).first()
                    crud.create_game_category(new_game.id, cat.id)
                except:
                    continue
        
        # Create Publisher objects for game's publishers
        # Get a list of publishers
        publishers_list = game["publishers"]

        # Iterate through the list, as long as it's not empty
        if len(publishers_list) > 0:
            for publisher in publishers_list:
                publisher = publisher.strip()
                # See if publisher already exists in db
                existing_pub = model.Publisher.query.filter_by(
                               name = publisher).first()
                if existing_pub:
                    crud.create_game_publisher(new_game.id, existing_pub.id)
                else:
                    new_pub = crud.create_publisher(publisher)
                    crud.create_game_publisher(new_game.id, new_pub.id)

        # Create Designers objects for game's designers
        # Get a list of designers
        designers_list = game["designers"]

        # Iterate through the list, as long as it's not empty
        if len(designers_list) > 0:
            for designer in designers_list:
                designer = designer.strip()
                # See if designer already exists in db
                existing_designer = model.Designer.query.filter_by(
                                    name = designer).first()
                if existing_designer:
                    crud.create_game_designer(new_game.id, 
                                              existing_designer.id)
                else:
                    new_designer = crud.create_designer(designer)
                    crud.create_game_designer(new_game.id, new_designer.id)

        # Create Artists objects for game's artists
        # Get a list of artists
        artists_list = game["artists"]

        # Iterate through the list, as long as it's not empty
        if len(artists_list) > 0:
            for artist in artists_list:
                artist = artist.strip()
                # See if artist already exists in db
                existing_artist = model.Artist.query.filter_by(
                                    name = artist).first()
                if existing_artist:
                    crud.create_game_artist(new_game.id, 
                                              existing_artist.id)
                else:
                    new_artist = crud.create_artist(artist)
                    crud.create_game_artist(new_game.id, new_artist.id)

# Using users_list and games_list, choose 3 random games for each user
# to seed the user_games table
for user in users_list:
    for game in range(3):
        random_game = choice(games_list)
        crud.create_user_game(user.id, random_game.id)




 
