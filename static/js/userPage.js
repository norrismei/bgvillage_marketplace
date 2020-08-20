"use strict";

// Load Own games view on first load of the page

$('#above-games-table').html(
    '<a href="/games">Search for games to add</a>'
);

const gamesTable = $('#games-table');

gamesTable.html(
        `<th>Sell</th>
         <th>Image</th>
         <th>Name</th>
         <th>Players</th>
         <th>Playtime</th>
         <th>Remove</th>`
    );
    $.get('/api/own_games.json', (response) => {
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

// Show the user's own games upon clicking on Own button
$('#own-button').on('click', () => {
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
    $.get('/api/own_games.json', (response) => {
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
});


// Show the games that the user is selling upon clicking on Sell button
$('#sell-button').on('click', () => {
    $('#above-games-table').html(
        'Options of games to sell here'
    );
    gamesTable.html(
        `<th>Image</th>
         <th>Name</th>
         <th>Condition</th>
         <th>Price</th>
         <th>Listing Comment</th>
         <th>Edit</th>`
    );
    $.get('/api/listed_games.json', (response) => {
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
});

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
    $.get('/api/wanted_games.json', (response) => {
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
