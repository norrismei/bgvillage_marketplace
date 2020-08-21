import requests

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


def add_game_to_database(atlas_id, add_type):
    """Adds game to either UserGame or WantedGame tables"""

    game_id = crud.get_game_id_by_atlas_id(atlas_id)

    added_game = False
    if add_type == "own":
        # Will need to replace 1 with username
        added_game = crud.create_user_game(1, game_id)
    elif add_type == "wishlist":
        added_game = crud.create_wanted_game(1, game_id)

    if added_game:
        return "Game was successfully added"
    else:
        return "A problem has occurred"