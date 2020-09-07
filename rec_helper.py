import crud

import model

import helper


def get_user_ever_own_game_ids(username):
    """Returns set of user's ever-owned user_games"""
    
    ever_own_games = crud.get_user_ever_own_games(username)
    ever_own_game_ids = helper.get_id_set(ever_own_games)

    return ever_own_game_ids


def analyze_games(games):
    """Takes in set of games and returns lists of top mechanics/categories"""

    mech_counts, cat_counts = count_mechs_categories(games)

    top_mechs = get_top_three(mech_counts)
    top_cats = get_top_three(cat_counts)

    return top_mechs, top_cats


def count_mechs_categories(games):
    """Takes in games and returns sorted lists of mechanics/categories by count

    For example, 
    sorted_mechs = [('Hand Management', 13), ('Dice Rolling', 10).....]
    sorted_cats = [('Adventure', 6), ('Puzzle', 5).....]"""

    mech_counts = {}
    cat_counts = {}
    
    for game in games:
        for mechanic in game.mechanics:
            mech_counts[mechanic.name] = mech_counts.get(mechanic.name, 0) + 1
        for category in game.categories:
            cat_counts[category.name] = cat_counts.get(category.name, 0) + 1

    sorted_mechs = sorted(mech_counts.items(), 
                          key=lambda x: x[1],
                          reverse=True)

    sorted_cats = sorted(cat_counts.items(),
                         key=lambda x: x[1],
                         reverse=True)

    return sorted_mechs, sorted_cats


def get_top_three(sorted_lst):
    """Take in sorted list of tuples and returns list of top 3 traits

    >>> get_top_three([('Hand Management', 13), ('Dice Rolling', 10), ('Tile Placement', 8), ('Worker Placement', 6)])
    ['Hand Management', 'Dice Rolling', 'Tile Placement']

    >>> get_top_three([('Hand Management', 13), ('Dice Rolling', 10)])
    ['Hand Management', 'Dice Rolling']

    >>> get_top_three([])
    []
    
    """

    top_three = []

    for i in range(3):
        try:
            top_three.append(sorted_lst[i][0])
        except:
            break

    return top_three


def find_game_matches(games, mechanics, categories):
    """Takes in games list and returns list of games with matching mechs/cats"""

    rec_ids = set([])
    criteria = set([])

    print(f"Categories: {categories}")

    for game in games:
        for mechanic in game.mechanics:
            if mechanic.name in mechanics:
                rec_ids.add(game.id)
                criteria.add(mechanic.name)
                print(f"added mech: {mechanic.name} criteria {criteria}")
        for category in game.categories:
            print(category.name)
            if category.name in categories:
                rec_ids.add(game.id)
                criteria.add(category.name)
                print(f"added category: {category.name} criteria {criteria}")
    return rec_ids, list(criteria)


def get_recs(listed_games, wanted_games, username):
    """Takes in listed games and returns recommended games based on user's lists"""

    ever_own_user_games = crud.get_user_ever_own_games(username)
    ever_own_games = helper.get_game_set(ever_own_user_games)

    rec_basis_games = wanted_games|ever_own_games
    rec_mechs, rec_cats = analyze_games(rec_basis_games)

    listed_games = helper.get_game_set(listed_games)

    games_to_consider = listed_games - rec_basis_games
    rec_ids, rec_criteria = find_game_matches(games_to_consider, rec_mechs, rec_cats)

    return rec_ids, rec_criteria


if __name__ == '__main__':
    from doctest import testmod
    if testmod().failed == 0:
        from server import app
        model.connect_to_db(app)