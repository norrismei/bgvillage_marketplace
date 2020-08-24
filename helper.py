import requests

import crud

import model

def search_board_game_atlas(search_terms):
    """Makes call to Board Game Atlas API using search terms"""

    payload = {'name': search_terms,
               'fields': 'id,name,min_players,max_players,publishers,image_url',
               'limit': '10',
               'fuzzy_match': 'True',
               'pretty': 'True',
               'client_id': 'ZRKfcqdFcV'}
    
    response = requests.get('https://api.boardgameatlas.com/api/search', params=payload)

    api_results = response.json()

    # Get the list of games returned
    games = api_results["games"]

    search_results = []
    for game in games:
        try:
            publisher = game["publishers"][0]
        except:
            publisher = ""

        search_results.append(
            {
            "key": game["id"],
            "name": game["name"],
            "min_players": game["min_players"],
            "max_players": game["max_players"],
            "publisher": publisher,
            "image_url": game["image_url"]
            }
        )

    return search_results


def add_game_to_database(add_type, name, atlas_id=None):
    """Adds game to either UserGame or WantedGame tables"""

    if atlas_id:
        #Check if there's record of this game in db with matching atlas id
        existing_game = crud.get_game_by_atlas_id(atlas_id)
        print(f"Existing game: {existing_game}")
    else:
        existing_game = crud.get_game_by_name(name)

    if existing_game:
        game_id = existing_game.id
    else:
        # If not in db, get object from Atlas API and save details in 
        # Game, GameMechanic, Category, GameCategory, Publisher, GamePublisher, 
        #Designer, and GameDesigner tables
        payload = {'ids': atlas_id,
                   'client_id': 'ZRKfcqdFcV'}
        response = requests.get('https://api.boardgameatlas.com/api/search', params=payload)
        print(response.url)
        new_game_response = response.json()
        new_game_data = new_game_response["games"][0]

        name = new_game_data["name"]
        description = new_game_data["description"]
        publish_year = new_game_data["year_published"]
        min_age = new_game_data["min_age"]
        min_players = new_game_data["min_players"]
        max_players = new_game_data["max_players"]
        min_playtime = new_game_data["min_playtime"]
        max_playtime = new_game_data["max_playtime"]
        image_url = new_game_data["image_url"]
        msrp = float(new_game_data["msrp"])
        atlas_id = new_game_data["id"]

        game = crud.create_game(name, description, publish_year, min_age,
                        min_players, max_players, min_playtime, max_playtime,
                        image_url, msrp, atlas_id)

        game_id = game.id

        # Create GameMechanic objects for game's mechanics
        # Get a list of dictionaries containing mechanic atlas_id's
        mechanics_list = new_game_data["mechanics"]

        # Iterate through the list, as long as it's not empty
        if len(mechanics_list) > 0:
            for mechanic in mechanics_list:
                atlas_id = mechanic["id"]
                # Try to match the atlas_id with what's in db to get mech id.
                # If can't find a match, skip it.
                try:
                    mech = model.db.session.query(model.Mechanic).filter_by(
                           atlas_id = atlas_id).first()
                    crud.create_game_mechanic(game_id, mech.id)
                except:
                    continue

        # Create GameCategory objects for game's categories
        # Get a list of dictionaries containing category atlas_id's
        categories_list = new_game_data["categories"]

        # Iterate through the list, as long as it's not empty
        if len(categories_list) > 0:
            for category in categories_list:
                atlas_id = category["id"]
                # Try to match the atlas_id with what's in db to get cat id.
                # If can't find a match, skip it.
                try:
                    cat = model.db.session.query(model.Category).filter_by(
                           atlas_id = atlas_id).first()
                    crud.create_game_category(game_id, cat.id)
                except:
                    continue
        
        # Create Publisher objects for game's publishers
        # Get a list of publishers
        publishers_list = new_game_data["publishers"]

        # Iterate through the list, as long as it's not empty
        if len(publishers_list) > 0:
            for publisher in publishers_list:
                publisher = publisher.strip()
                # See if publisher already exists in db
                existing_pub = model.Publisher.query.filter_by(
                               name = publisher).first()
                if existing_pub:
                    crud.create_game_publisher(game_id, existing_pub.id)
                else:
                    new_pub = crud.create_publisher(publisher)
                    crud.create_game_publisher(game_id, new_pub.id)

        # Create Designers objects for game's designers
        # Get a list of designers
        designers_list = new_game_data["designers"]

        # Iterate through the list, as long as it's not empty
        if len(designers_list) > 0:
            for designer in designers_list:
                designer = designer.strip()
                # See if designer already exists in db
                existing_designer = model.Designer.query.filter_by(
                                    name = designer).first()
                if existing_designer:
                    crud.create_game_designer(game_id, 
                                              existing_designer.id)
                else:
                    new_designer = crud.create_designer(designer)
                    crud.create_game_designer(game_id, new_designer.id)

    #After assigning game_id above, can add game to UserGame or WantedGame
    added_game = False
    if add_type == "own":
        # Will need to replace 1 with username
        added_game = crud.create_user_game(1, game_id)
    elif add_type == "wishlist":
        added_game = crud.create_wanted_game(1, game_id)

    print(f"Added game: {added_game}")
    
    if added_game:
        return "Game was successfully added"
    else:
        return "A problem has occurred"


def get_user_own_games(username):
    """Returns list of user's own games as dictionary"""

    own_games = crud.get_user_own_games(username)

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

    return results


def get_user_listed_games(username):
    """Returns list of user's listed games as dictionary"""

    listed_games = crud.get_user_listed_games(username)

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

    return results


def handle_user_wanted_games(username):
    """Returns list of user's wanted games as dictionary"""

    wanted_games = crud.get_wanted_games(username)

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


def remove_game(remove_type, game_id):
    """Updates UserGame to own=False or deletes WantedGame"""

    removed_game = False
    if remove_type == "own":
        listed_game = crud.get_listed_game_by_id(game_id)
        if listed_game:
            crud.delete_listed_game(listed_game.id)
        removed_game = crud.update_user_game_to_false(game_id)
    elif remove_type == "wishlist":
        removed_game = crud.delete_wanted_game(game_id)

    if removed_game:
        return "Game was successfully removed"
    else:
        return "A problem has occurred"


def search_marketplace_listings(search_terms):
    """Returns all matching listings (by name) as dictionary"""

    listed_games = crud.get_marketplace_listings(search_terms)

    results = []

    for listed_game in listed_games:
        results.append(
            {
            "key": listed_game.id,
            "name": listed_game.user_game.game.name,
            "condition": listed_game.condition,
            "price": listed_game.price,
            "comment": listed_game.comment,
            "image_url": listed_game.user_game.game.image_url,
            "username": listed_game.user_game.user.username
            }
        )

    return results


