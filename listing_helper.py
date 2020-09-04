import crud

import model

import helper
import format_helper


def get_user_listed_games(username):
    """Returns list of user's listed games as dictionary"""

    listed_games = crud.get_user_listed_games(username)

    results = []

    for listed_game in listed_games:
        price = format_helper.format_price(listed_game.price)
        msrp = format_helper.format_msrp(listed_game.game)
        comment = format_helper.format_comment(listed_game)
        results.append(
            {
            "key": listed_game.user_games_id,
            "name": listed_game.game.name,
            "condition": listed_game.condition,
            "price": price,
            "username": listed_game.user.username,
            "email": listed_game.user.email,
            "comment": comment,
            "image_url": listed_game.game.image_url,
            "msrp": msrp
            }
        )

    return results
    

def get_user_games_able_to_sell(username):
    """Returns list of user's games available to sell, as dictionary"""

    own_games = crud.get_user_current_own_games(username)
    listed_games = crud.get_user_listed_games(username)

    listed_game_ids = []
    for listed_game in listed_games:
        listed_game_ids.append(listed_game.user_games_id)

    results = []

    for game in own_games:
        if game.id not in listed_game_ids:
            msrp = format_helper.format_msrp(game.game)
            results.append(
                {
                "key": game.id,
                "name": game.game.name,
                "msrp": msrp,
                "image_url": game.game.image_url
                }
            )
                    
    return results


def list_game(user_game_id, condition, price, comment):
    """Creates new listed game and returns listed game as dictionary"""

    previously_listed = crud.get_listed_game_by_id(user_game_id)

    if previously_listed:
        reactivated = crud.update_listed_game_to_true(user_game_id)
        listed_game = crud.update_listed_game(user_game_id, condition, price, comment)
    else:
        listed_game = crud.create_listed_game(user_game_id, condition, price, comment)

    price = format_helper.format_price(listed_game.price)
    msrp = format_helper.format_msrp(listed_game.game)
    comment = format_helper.format_comment(listed_game)

    return {
        "key": listed_game.user_games_id,
        "name": listed_game.game.name,
        "condition": listed_game.condition,
        "price": price,
        "username": listed_game.user.username,
        "email": listed_game.user.email,
        "comment": comment,
        "image_url": listed_game.game.image_url,
        "msrp": msrp    
    }


def update_user_listed_game(user_game_id, condition, price, comment):
    """Updates listed game and returns updates as dictionary"""

    updated_game = crud.update_listed_game(user_game_id, condition, price, comment)

    price = format_helper.format_price(updated_game.price)
    comment = format_helper.format_comment(updated_game)

    return {
        "key": updated_game.user_games_id,
        "condition": updated_game.condition,
        "price": price,
        "comment": comment
    }


def deactivate_listing(user_game_id):
    """Updates ListedGame active=False and returns removed ListedGame as dict"""

    deactivated_listing = crud.update_listed_game_to_false(user_game_id)

    msrp = format_helper.format_msrp(deactivated_listing.game)


    return {
        "key": deactivated_listing.user_games_id,
        "name": deactivated_listing.game.name,
        "msrp": msrp,
        "image_url": deactivated_listing.game.image_url
    }



if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)