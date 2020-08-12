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
 
