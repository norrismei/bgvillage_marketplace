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
            gamesTable.append(
                `<tr id="list-row-${game.key}">
                    <td class="list-row-img" width="20%">
                        <img src=${game.image_url} height="50"/>
                    </td>
                    <td class="list-row-name">${game.name}</td>
                    <td class="list-row-condition">${game.condition}</td>
                    <td class="list-row-price" 
                        data-msrp=${game.msrp}>${game.price}</td>
                    <td class="list-row-comment">${game.comment}</td>
                    <td>
                        <button class="select-edit-listing" data-game-id=${game.key}>
                            Edit
                        </button>
                    </td>
                </tr>`
            );
        };
    });
}

function createListingForm(imgURL,gId, gName, msrp, bClass, bText) {
    $('#user-list-img').html(`<img src=${imgURL} height="150" />`);
    $('#user-list-game-name').html(`<h2 key=${gId}>${gName}</h2>`);
    $('#user-list-msrp').html(`MSRP: $${msrp}`);
    $('#user-list-button').html(`<button type="submit" class="${bClass}">
                                    ${bText}
                                 </button>`);
}

function createListingFormData() {
    const gameId = listingForm.children('#user-list-game-name').children().attr('key')
    const data = {
        'game': gameId,
        'condition': $('#listing-condition').val(),
        'price': $('#listing-price').val(),
        'comment': $('#listing-comment').val()
    };
    return data;
}

function clearListingForm() {
    $('#listing-condition option:first').prop('selected', true);
    $('#listing-price').val("");
    $('#listing-comment').val("");
    $('#user-list-delete').remove();
}

function tearDownListingForm() {
    modal.hide();
    clearListingForm();
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
const listingForm = $('#listing-form');
const close = $('.close');

close.on('click', (event) => {
    modal.hide();
    clearListingForm();
})

// When user clicks button to create listing, open modal with create listing form
$('#above-games-table').on('click', '#create-listing-button', (event) => {
    event.preventDefault();
    const createListingButton = $(event.target);
    const gameSelector = createListingButton.siblings('#own-game-selector');
    const gameId = gameSelector.val();
    const gameImageURL = gameSelector.children(':selected').attr('data-img');
    const gameName = gameSelector.children(':selected').text();
    const gameMSRP = gameSelector.children(':selected').attr('data-msrp');
    const buttonClass = 'create-listing'
    const buttonText = 'Submit'
    createListingForm(gameImageURL, gameId, gameName, gameMSRP, 
                      buttonClass, buttonText);
    modal.show();
})

// When user clicks button to edit listing, open modal with edit listing form
gamesTable.on('click', 'button.select-edit-listing', (event) => {
    event.preventDefault();
    const editListingButton = $(event.target);
    const gameId = editListingButton.attr('data-game-id');
    const gameImageURL = editListingButton.parent().siblings(
                         '.list-row-img').children('img').attr('src');
    const gameName = editListingButton.parent().siblings('.list-row-name').html();
    const msrp = editListingButton.parent().siblings('.list-row-price').attr('data-msrp');
    const buttonClass = 'edit-listing'
    const buttonText = 'Save'
    createListingForm(gameImageURL, gameId, gameName, msrp, 
                      buttonClass, buttonText);
    const condition = editListingButton.parent().siblings(
                      '.list-row-condition').html();
    const price = editListingButton.parent().siblings('.list-row-price').html();
    const comment = editListingButton.parent().siblings(
                          '.list-row-comment').html();
    $('#listing-condition').val(condition);
    $('#listing-price').val(price);
    $('#listing-comment').val(comment);
    listingForm.append(`<p class="list-details" id="user-list-delete">
                            <a href="/api/deactivate-listing">Keep game, remove listing</a>
                        </p>`);
    modal.show();
})


// When user fills out form and clicks on button to submit, send POST request to 
// server to create ListedGame in database and re-render listings table on page
listingForm.on('click', 'button.create-listing', (event) => {
    event.preventDefault();
    const data = createListingFormData();
    $.post("/api/list-game", data, (response) => {
        gamesTable.append(
                `<tr id="list-row-${response.key}">
                    <td class="list-row-img" width="20%">
                        <img src=${response.image_url} height="50"/>
                    </td>
                    <td class="list-row-name">${response.name}</td>
                    <td class="list-row-condition">${response.condition}</td>
                    <td class="list-row-price" 
                        data-msrp=${response.msrp}>${response.price}</td>
                    <td class="list-row-comment">${response.comment}</td>
                    <td>
                        <button class="select-edit-listing" data-game-id=${response.key}>
                            Edit
                        </button>
                    </td>
                </tr>`
        );
        $('#own-game-selector').children(':selected').remove();
        $('#own-game-selector option:first').prop('selected', true);
        tearDownListingForm();
    });
})
// When user edits listing form and clicks on save button, send POST request to 
// server to update ListedGame in database and re-render just the row to
// reflect changes
listingForm.on('click', 'button.edit-listing', (event) => {
    event.preventDefault();
    const data = createListingFormData();
    $.post("/api/update-listing", data, (response) => {
        const updatedRow = $(`#list-row-${response.key}`);
        updatedRow.children('.list-row-condition').html(response.condition);
        updatedRow.children('.list-row-price').html(response.price);
        updatedRow.children('.list-row-comment').html(response.comment);
        tearDownListingForm();
    });
})

// When user clicks on link to delete listing, send POST request to server to 
// update ListedGame in database and remove row
listingForm.on('click', '#user-list-delete', (event) => {
    event.preventDefault();
    const gameId = listingForm.children(
                   '#user-list-game-name').children().attr('key');
    $.post("/api/deactivate-listing", {'user_game_id': gameId}, (response) => {
        const removeRow = $(`#list-row-${response.key}`);
        removeRow.remove();
        $('#own-game-selector').append(
            `<option value=${response.key} data-msrp=${response.msrp} data-img=${response.image_url}>
                ${response.name}
            </option>`);
        tearDownListingForm();
    })
})


