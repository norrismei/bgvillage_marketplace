import crud

import model

import helper

def format_players(game):
    """Takes in game object and returns formatted player count"""

    min_players = game.min_players
    max_players = game.max_players

    num_players = []
    if min_players:
        num_players = min_players
        if max_players and (max_players != min_players):
            num_players = f"{min_players}-{max_players}"
        return num_players
    else:
        return ""


def format_playtime(game):
    """Takes in game object and returns formatted playtime"""

    min_playtime = game.min_playtime
    max_playtime = game.max_playtime

    playtime = []
    if min_playtime:
        playtime = min_playtime
        if max_playtime and (max_playtime != min_playtime):
            playtime = f"{min_playtime}-{max_playtime} mins"
        return playtime
    else:
        return ""


def format_msrp(game):
    """Takes in game object and returns formatted msrp"""

    msrp = game.msrp

    if msrp and msrp > 0:
        return msrp
    else:
        return ""


def format_comment(listed_game):
    """Takes in ListedGame object and returns formatted comment"""

    comment = listed_game.comment

    if comment:
        return comment
    else:
        return ""


def format_publishers(game):
    """Takes in game object and returns primary publisher name"""

    publishers_list = game.publishers

    try:
        return publishers_list[0].name
    except:
        return ""


def format_designers(game):
    """Takes in game object and returns list of designers as string"""

    designers = game.designers
    designer_names = []

    for designer in designers:
        if designer and designer.name:
            designer_names.append(designer.name)

    if len(designer_names) > 1:
        designers_list_str = ", ".join(designer_names)
        return designers_list_str
    elif len(designer_names) == 1:
        return designer_names[0]
    else:
        return ""


def format_mechanics(game):
    """Takes in game object and returns list of mechanics as string"""

    mechanics = game.mechanics
    mechanic_names = []

    for mechanic in mechanics:
        if mechanic and mechanic.name:
            mechanic_names.append(mechanic.name)

    if len(mechanic_names) > 1:
        mechanics_list_str = ", ".join(mechanic_names)
        return mechanics_list_str
    elif len(mechanic_names) == 1:
        return mechanic_names[0]
    else:
        return ""


def format_categories(game):
    """Takes in game object and returns list of categories as string"""

    categories = game.categories
    category_names = []

    for category in categories:
        if category and category.name:
            category_names.append(category.name)

    if len(category_names) > 1:
        categories_list_str = ", ".join(category_names)
        return categories_list_str
    elif len(category_names) == 1:
        return category_names[0]
    else:
        return ""


def format_price(price):
    """Takes in price and formats as str with two decimal places"""

    formatted_price = "{:.2f}".format(price)

    return formatted_price
    

if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)