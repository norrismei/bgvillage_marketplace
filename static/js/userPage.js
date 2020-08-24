"use strict";

const gamesTable = $('#games-table');

function displayOwnView() {
    $('#above-games-table').html(
        '<a href="/games">Search for games to add</a>'
    );

    gamesTable.html(
            `<th>Sell</th>
             <th>Image</th>
             <th>Name</th>
             <th>Players</th>
             <th>Playtime</th>
             <th>Remove</th>`
        );

    $.get('/api/user/own_games.json', (response) => {
        for (const game of response) {
            let players = [];
            if (game.min_players) {
                players = `${game.min_players}`;
                if (game.max_players && 
                    game.max_players != game.min_players) {
                    players = `${game.min_players}-${game.max_players}`
                };
            };
            let playtime = [];
            if (game.min_playtime) {
                playtime = `${game.min_playtime} mins`;
                if (game.max_playtime && 
                    game.max_playtime != game.min_playtime) {
                    playtime = `${game.min_playtime}-${game.max_playtime} mins`
                };
            };
            gamesTable.append(
                `<tr>
                    <td></td>
                    <td><img src=${game.image_url} height="50" /></td>
                    <td>${game.name}</td>
                    <td>${players}</td>
                    <td>${playtime}</td>
                    <td>
                        <button class="remove from-own" 
                                data-game-id=${game.key}>
                            Remove
                        </button>
                    </td>
                </tr>`
            );
        };
    });
}


function displaySellView() {
    $('#above-games-table').html(
        `<div>
            <form id="listing-form">
                <select name="game" id="own-game-selector">
                </select>
                <select name="condition">
                    <option value="" disabled selected>Game Condition</option>
                    <option value="New">New</option>
                    <option value="Like New">Like New</option>
                    <option value="Very Good">Very Good</option>
                    <option value="Good">Good</option>
                    <option value="Acceptable">Acceptable</option>
                </select>
                <input type="text" 
                       name="price" 
                       placeholder="Enter Price">
                </input>
                <input type="text" 
                       name="comment" 
                       placeholder="Optional Comment">
                </input>
                <button type="submit">Create listing</button>
            </form>
        </div>`
    );
    $.get('/api/user/own_games.json', (response) => {
        $('#own-game-selector').html(
                    '<option value="" disabled selected>Choose game</option');
        for (const game of response) {
            $('#own-game-selector').append(
                    `<option value=${game.key}>${game.name}</option>`)
        }
    })
    gamesTable.html(
        `<th>Image</th>
         <th>Name</th>
         <th>Condition</th>
         <th>Price</th>
         <th>Listing Comment</th>
         <th>Edit</th>`
    );
    $.get('/api/user/listed_games.json', (response) => {
        for (const game of response) {
            let comment = []
            if (game.comment) {
                comment = game.comment
            }
            gamesTable.append(
                `<tr>
                    <td width="20%"><img src=${game.image_url} height="50"/></td>
                    <td>${game.name}</td>
                    <td>${game.condition}</td>
                    <td>${game.price}</td>
                    <td>${comment}</td>
                    <td></td>
                </tr>`
            );
        };
    });
}

// Load Own games view on first load of the page
displayOwnView();

// Show the user's own games upon clicking on Own button
$('#own-button').on('click', () => {
    displayOwnView();
});

// After clicking on sell button, show form to create game listing, 
// followed by table showing games user has listed for sale
$('#sell-button').on('click', () => {
    displaySellView();
});
    

// When user submits form to create listing, send POST request to server
// to create ListedGame in database and re-render listings table on page
$('#above-games-table').on('submit', '#listing-form', (event) => {
    event.preventDefault();
    const formValues = $('#listing-form').serialize();
    $.post("/api/list-game", formValues, (response) => {
        displaySellView();
    })
})

// Show the user's wishlist upon clicking on Wishlist button
$('#wishlist-button').on('click', () => {
    $('#above-games-table').html(
        '<a href="/games">Search for games to add</a>'
    );
    gamesTable.html(
        `<th>Image</th>
         <th>Name</th>
         <th>Players</th>
         <th>Playtime</th>
         <th>Remove</th>`
    )
    $.get('/api/user/wanted_games.json', (response) => {
        for (const game of response) {
            let players = [];
            if (game.min_players) {
                players = `${game.min_players}`;
                if (game.max_players && 
                    game.max_players != game.min_players) {
                    players = `${game.min_players}-${game.max_players}`
                };
            };
            let playtime = [];
            if (game.min_playtime) {
                playtime = `${game.min_playtime} mins`;
                if (game.max_playtime) {
                    playtime = `${game.min_playtime}-${game.max_playtime} mins`
                };
            };
            gamesTable.append(
                `<tr>
                    <td><img src=${game.image_url} height="50" /></td>
                    <td>${game.name}</td>
                    <td>${players}</td>
                    <td>${playtime}</td>
                    <td>
                        <button class="remove from-wishlist" 
                                data-game-id=${game.key}>
                            Remove
                        </button>
                    </td>
                </tr>`
            );
        };
    });
});

// An example of event delegation. If we selected the buttons, which are
// dynamically produced, the event handler won't bind to them. Instead, select
// the parent element and move the button selector to second parameter of .on()
// method.
$('#games-table').on('click', 'button.remove', (event) => {
    const removeButton = $(event.target);
    const removeButtonId = removeButton.attr('data-game-id');
    if (removeButton.hasClass('from-own')) {
        $.post('/api/remove-game', {'user_game_id': removeButtonId,
                                    'remove_type': 'own'}, (res) => {
        removeButton.closest('tr').remove();
        });
    };
    if (removeButton.hasClass('from-wishlist')) {
        $.post('/api/remove-game', {'user_game_id': removeButtonId,
                                    'remove_type': 'wishlist'}, (res) => {
        removeButton.closest('tr').remove();
        });
    };
    
})
