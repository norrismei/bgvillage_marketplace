"""Script to seed database"""

import os
import json
from datetime import datetime

import crud
import model
import server

os.system('dropdb bgvillage')
os.system('createdb bgvillage')

model.connect_to_db(server.app)
model.db.create_all()

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

        crud.create_user(username, fname, lname, email, password, birthdate)

with open('data/mechanics.json') as f:
    mechanic_data = json.loads(f.read())

    for mechanic in mechanic_data:
        name = mechanic["name"]
        atlas_id = mechanic["id"]

        crud.create_mechanic(name, atlas_id)

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
        msrp = game["msrp"]

        crud.create_game(name, description, publish_year, min_age,
                        min_players, max_players, min_playtime, max_playtime,
                        image_url, msrp)


 
