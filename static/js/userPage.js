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

    $.get('/api/user/own-games.json', (response) => {
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
            <form id="select-game-to-sell-form">
                <select name="game" id="own-game-selector">
                </select>
                </input>
                <button type="submit" id="create-listing-button">
                    Create listing
                </button>
            </form>
        </div>`
    );
    // $('#above-games-table').html(
    //     `<div>
    //         <form id="listing-form">
    //             <select name="game" id="own-game-selector">
    //             </select>
                // <select name="condition">
                //     <option value="" disabled selected>Game Condition</option>
                //     <option value="New">New</option>
                //     <option value="Like New">Like New</option>
                //     <option value="Very Good">Very Good</option>
                //     <option value="Good">Good</option>
                //     <option value="Acceptable">Acceptable</option>
                // </select>
                // <input type="text" 
                //        name="price" 
                //        placeholder="Enter Price">
                // </input>
                // <input type="text" 
                //        name="comment" 
                //        placeholder="Optional Comment">
                // </input>
    //             <button type="submit">Create listing</button>
    //         </form>
    //     </div>`
    // );
    $.get('/api/user/own-games/to-sell.json', (response) => {
        $('#own-game-selector').html(
                    '<option value="" disabled selected>Choose game</option');
        for (const game of response) {
            $('#own-game-selector').append(
                    `<option value=${game.key} data-msrp=${game.msrp} data-img=${game.image_url}>
                        ${game.name}
                     </option>`);
        };
    });
    gamesTable.html(
        `<th>Image</th>
         <th>Name</th>
         <th>Condition</th>
         <th>Price</th>
         <th>Listing Comment</th>
         <th>Edit</th>`
    );
    $.get('/api/user/listed-games.json', (response) => {
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
                    <td>
                        <button class="edit-listing" data-game-id=${game.key}>
                            Edit
                        </button>
                    </td>
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
    

// When user clicks button to create listing, open modal with create listing form
$('#above-games-table').on('click', '#create-listing-button', (event) => {
    event.preventDefault();
    const createListingButton = $(event.target);
    const gameSelector = createListingButton.siblings('#own-game-selector');
    const gameId = gameSelector.val();
    const gameImageURL = gameSelector.children(':selected').attr('data-img');
    const gameName = gameSelector.children(':selected').text();
    const gameMSRP = gameSelector.children(':selected').attr('data-msrp');
    console.log(gameMSRP);
    $('#user-list-img').html(`<img src=${gameImageURL} height="150" />`);
    $('#user-list-game-name').html(`<h2 key=${gameId}>${gameName}</h2>`);
    $('#user-list-msrp').html(`MSRP: $${gameMSRP}`);
    $('#user-list-button').html(`<button type="submit" class="create-listing" id="create-listing-button">
                                    Submit
                                 </button>`);
    modal.show();
})
// $('#above-games-table').on('submit', '#listing-form', (event) => {
//     event.preventDefault();
//     const formValues = $('#listing-form').serialize();
//     $.post("/api/list-game", formValues, (response) => {
//         displaySellView();
//     })
// })

// When user fills out form and clicks on button to submit, send POST request to 
// server to create ListedGame in database and re-render listings table on page

const listingForm = $('#listing-form');
listingForm.on('click', 'button.create-listing', (event) => {
    event.preventDefault();
    const gameId = listingForm.children('#user-list-game-name').children().attr('key')
    const data = {
        'game': gameId,
        'condition': $('#listing-condition').val(),
        'price': $('#listing-price').val(),
        'comment': $('#listing-comment').val()
    };
    $.post("/api/list-game", data, (response) => {
        modal.hide();
        $('#listing-condition option:first').prop('selected', true);
        $('#listing-price').val("");
        $('#listing-comment').val("");
        displaySellView();
    });
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
    $.get('/api/user/wanted-games.json', (response) => {
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

// <---------------------Event handler for modal------------------------>
const modal = $('.modal');
const modalBody = $('.modal-body');
const close = $('.close');

close.on('click', (event) => {
    modal.hide();
    // $('.list-details').empty();
})


