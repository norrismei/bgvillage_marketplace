"use strict";

const gamesTable = $('#games-table');

// Load the gamesTable on first load of the page
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
            let playtime = null;
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
                    <td>${game.min_players}-${game.max_players}</td>
                    <td>${playtime}</td>
                    <td></td>
                </tr>`
            );
        };
    });

// Show the user's own games upon clicking on Own button
$('#own-button').on('click', () => {
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
            let playtime = null;
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
                    <td>${game.min_players}-${game.max_players}</td>
                    <td>${playtime}</td>
                    <td></td>
                </tr>`
            );
        };
    });
});


// Show the games that the user is selling upon clicking on Sell button
$('#sell-button').on('click', () => {
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
            gamesTable.append(
                `<tr>
                    <td width="20%"><img src=${game.image_url} height="50"/></td>
                    <td>${game.name}</td>
                    <td>${game.condition}</td>
                    <td>${game.price}</td>
                    <td>${game.comment}</td>
                    <td></td>
                </tr>`
            );
        };
    });
});

// Show the user's wishlist upon clicking on Wishlist button
$('#wishlist-button').on('click', () => {
    gamesTable.html(
        `<th>Image</th>
         <th>Name</th>
         <th>Players</th>
         <th>Playtime</th>
         <th>Remove</th>`
    )
    $.get('/api/wanted_games.json', (response) => {
        for (const game of response) {
            let playtime = null;
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
                    <td>${game.min_players}-${game.max_players}</td>
                    <td>${playtime}</td>
                    <td></td>
                </tr>`
            );
        };
    });
});
