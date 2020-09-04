import crud

import model

import helper
import format_helper
import rec_helper


def search_marketplace_listings(search_terms, username):
    """Returns all matching listings (by name) as dictionary list"""

    listed_games = crud.get_marketplace_listings(search_terms)

    wanted = crud.get_user_wanted_games(username)
    wanted_game_ids = helper.get_id_set(wanted)
    wanted_games = helper.get_game_set(wanted)

    rec_game_ids, rec_criteria = rec_helper.get_recs(listed_games, wanted_games, username)
    
    # We want to include info about whether a game is on a user's 
    # wishlist, so we pass in the username to our function
    results = create_listings_dict(listed_games, wanted_game_ids,
                                   rec_game_ids)

    return results


def create_listings_dict(listings, wanted_games, rec_games):
    """Formats listings info, along with wishlist and rec data, into dict"""

    results = []

    for listed_game in listings:
        price = format_helper.format_price(listed_game.price)
        
        wishlist = False
        if listed_game.game.id in wanted_games:
            wishlist = True
        
        recommended = False
        if listed_game.game.id in rec_games:
            recommended = True
        
        results.append(
            {
            "key": listed_game.id,
            "name": listed_game.user_game.game.name,
            "condition": listed_game.condition,
            "price": price,
            "comment": listed_game.comment,
            "image_url": listed_game.user_game.game.image_url,
            "username": listed_game.user_game.user.username,
            "wishlist": wishlist,
            "recommended": recommended
            }
        )

    return results


def get_listing_details(listing_id, username):
    """Returns details of a listing as a dictionary"""

    listing = crud.get_listing_details(listing_id)
    game = listing.user_game.game

    selling_other_games = False
    all_games = crud.get_user_listed_games(username)
    if len(all_games) > 1:
        selling_other_games = True

    price = format_helper.format_price(listing.price) 
    comment = format_helper.format_comment(listing)

    players = format_helper.format_players(game)
    playtime = format_helper.format_playtime(game)
    msrp = format_helper.format_msrp(game)
    primary_publisher = format_helper.format_publishers(game)
    designers = format_helper.format_designers(game)
    mechanics = format_helper.format_mechanics(game)
    categories = format_helper.format_categories(game)

    return {
        "key": listing.id,
        "image_url": listing.game.image_url,
        "game_name": listing.game.name,
        "condition": listing.condition,
        "price": price,
        "msrp": msrp,
        "username": listing.user.username,
        "email": listing.user.email,
        "comment": comment,
        "min_age": listing.game.min_age,
        "players": players,
        "playtime": playtime,
        "publisher": primary_publisher,
        "designers": designers,
        "publish_year": listing.game.publish_year,
        "game_description": listing.game.description,
        "mechanics": mechanics,
        "categories": categories,
        "other_games": selling_other_games
    }


def filter_listings_by_username(user, selected_username):
    """Returns a single user's listings as a dictionary"""

    filtered_listings = crud.get_user_listed_games(selected_username)

    wanted = crud.get_user_wanted_games(user)
    wanted_game_ids = helper.get_id_set(wanted)
    wanted_games = helper.get_game_set(wanted)
    rec_game_ids, rec_criteria = rec_helper.get_recs(filtered_listings, 
                                          wanted_games, 
                                          user)

    results = create_listings_dict(filtered_listings, 
                                   wanted_game_ids, 
                                   rec_game_ids)

    return results


if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)