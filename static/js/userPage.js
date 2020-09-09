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
            let players = "";
            if (game.min_players) {
                players = `${game.min_players}`;
                if (game.max_players && 
                    game.max_players != game.min_players) {
                    players = `${game.min_players}-${game.max_players}`
                };
            };
            let playtime = "";
            if (game.min_playtime) {
                playtime = `${game.min_playtime} mins`;
                if (game.max_playtime && 
                    game.max_playtime != game.min_playtime) {
                    playtime = `${game.min_playtime}-${game.max_playtime} mins`
                };
            };
            let selling = ""
            if (game.selling) {
                selling = `<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                            </svg>`
            };
            gamesTable.append(
                `<tr data-usergame-id=${game.key}>
                    <td>${selling}</td>
                    <td><img src=${game.image_url} height="50" /></td>
                    <td class="game-name">${game.name}</td>
                    <td>${players}</td>
                    <td>${playtime}</td>
                    <td>
                        <button type="button" class="btn remove from-own" 
                                data-game-id=${game.key}>
                            <svg width="1.5em" height="1.5em" viewBox="0 0 16 16" class="bi bi-trash" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                              <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                            </svg>
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
                <button type="submit" id="create-listing-button" class="btn btn-primary" disabled>
                    Create listing
                </button>
            </form>
        </div>`
    );
    $.get('/api/user/own-games/to-sell.json', (response) => {
        $('#own-game-selector').html(
                    '<option value="" selected disabled>Choose game</option');
        for (const game of response) {
            $('#own-game-selector').append(
                    `<option value="${game.key}" data-msrp="${game.msrp}" data-img="${game.image_url}">
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
                        <img src="${game.image_url}" height="50"/>
                    </td>
                    <td class="list-row-name">${game.name}</td>
                    <td class="list-row-condition">${game.condition}</td>
                    <td class="list-row-price" 
                        data-msrp="${game.msrp}">${game.price}</td>
                    <td class="list-row-comment">${game.comment}</td>
                    <td>
                        <button type="button" class="btn select-edit-listing" data-game-id=${response.key}>
                            <svg width="1.5em" height="1.5em" viewBox="0 0 16 16" class="bi bi-pencil-square" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456l-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                              <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                            </svg>
                        </button>
                    </td>
                </tr>`
            );
        };
    });
}

function createListingForm(imgURL, gId, gName, msrp, bClass, bText) {
    $('#user-list-img').html(`<img src=${imgURL} height="150" />`);
    $('#user-list-game-name').html(`<h2 key=${gId}>${gName}</h2>`);
    if (msrp) {
        $('#user-list-msrp').html(`MSRP: ${msrp}`);
    };
    $('#user-list-button').addClass(`${bClass}`);
    $('#user-list-button').html(`${bText}`);
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
    $('#user-list-button').removeClass();
    $('#user-list-button').empty();
}

function tearDownListingForm() {
    sellModal.modal('hide');
    clearListingForm();
}

function createListing(data) {
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
                        <button type="button" class="btn select-edit-listing" data-game-id=${response.key}>
                            <svg width="1.5em" height="1.5em" viewBox="0 0 16 16" class="bi bi-pencil-square" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456l-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                              <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                            </svg>
                        </button>
                    </td>
                </tr>`
        );
        $('#own-game-selector').children(':selected').remove();
        $('#own-game-selector option:first').prop('selected', true);
        tearDownListingForm();
    });
}

function editListing(data) {
    $.post("/api/update-listing", data, (response) => {
        const updatedRow = $(`#list-row-${response.key}`);
        updatedRow.children('.list-row-condition').html(response.condition);
        updatedRow.children('.list-row-price').html(response.price);
        updatedRow.children('.list-row-comment').html(response.comment);
        tearDownListingForm();
    });
}

// Load Own games view on first load of the page
displayOwnView();


// Show the user's own games upon clicking on Own button
$('#own-button').on('click', () => {
    displayOwnView();
});

// After clicking on sell button, show table with games user has listed for sale
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
                        <button type="button" class="btn remove from-wishlist" 
                                data-game-id=${game.key}>
                            <svg width="1.5em" height="1.5em" viewBox="0 0 16 16" class="bi bi-trash" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                              <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                            </svg>
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
    console.log(event.target)
    const removeButton = $(event.target).closest('button');
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

// **************** Modals section ***********************

const sellModal = $('#sell-modal');
const ownModal = $('#own-modal')
const modal = $('.modal');
const modalBody = $('.modal-body');

// <---------------Event handler for game details modal------------------------>

gamesTable.on('click', '.game-name', (event) => {
    const userGame = $(event.target);
    const userGameId = userGame.parents().attr('data-usergame-id');
    const data = {"user_game_id": userGameId};
    $.get('/api/user/own-games/details.json', data, (response) => {
        $('#user-game-img').html(`<img src=${response.image_url} height="150" />`);
        $('#user-game-name').html(response.game_name);
        if (response.msrp) {
            $('#user-game-msrp').html(`MSRP: ${response.msrp}`);
        }
        if (response.min_age) {
            $('#user-game-min-age').html(`Min age: ${response.min_age}`);
        };
        if (response.players) {
            $('#user-game-players').html(`Players: ${response.players}`);
        };
        if (response.playtime) {
            $('#user-game-playtime').html(`Playtime: ${response.playtime}`);
        };
        if (response.publisher) {
            $('#user-game-publisher').html(`Publisher: ${response.publisher}`);
        };
        if (response.designers) {
            $('#user-game-designers').html(`Designers: ${response.designers}`);
        };
        if (response.publish_year) {
            $('#user-game-year').html(`Year Published: ${response.publish_year}`);
        };    
        // if (response.game_description) {
        //     $('#list-description').html(response.game_description);
        // }
        if (response.mechanics) {
            $('#user-game-mechanics').html(`Mechanics: ${response.mechanics}`);
        };
        if (response.categories) {
            $('#user-game-categories').html(`Categories: ${response.categories}`);
        };
        ownModal.modal({backdrop: true});
    })
});

// <---------------Event handler for listing modal------------------------>
const listingForm = $('#listing-form');

sellModal.on('hide.bs.modal', (event) => {
    clearListingForm();
})

// When user chooses game from the selector, create listing button is enabled.
$('#above-games-table').on('change', '#own-game-selector', (event) => {
    const createListingButton = $(event.target).siblings('#create-listing-button');
    if ($(event.target).val() === "") {
        createListingButton.attr('disabled', true);
    } else { createListingButton.removeAttr('disabled'); }
})

// When user clicks button to create listing, open modal with create listing form
$('#above-games-table').on('submit', '#select-game-to-sell-form', (event) => {
    event.preventDefault();
    const createListingButton = $(event.target).children('#create-listing-button');
    const gameSelector = createListingButton.siblings('#own-game-selector');
    const gameId = gameSelector.val();
    const gameImageURL = gameSelector.children(':selected').attr('data-img');
    const gameName = gameSelector.children(':selected').text();
    const gameMSRP = gameSelector.children(':selected').attr('data-msrp');
    const buttonClass = 'btn btn-primary create-listing'
    const buttonText = 'Submit'
    createListingForm(gameImageURL, gameId, gameName, gameMSRP, 
                      buttonClass, buttonText);
    sellModal.modal({backdrop: true});
})

// When user clicks button to edit listing, open modal with edit listing form
gamesTable.on('click', 'button.select-edit-listing', (event) => {
    event.preventDefault();
    const editListingButton = $(event.target).closest('button');
    const gameId = editListingButton.attr('data-game-id');
    const gameImageURL = editListingButton.parent().siblings(
                         '.list-row-img').children('img').attr('src');
    const gameName = editListingButton.parent().siblings('.list-row-name').html();
    const msrp = editListingButton.parent().siblings('.list-row-price').attr('data-msrp');
    const buttonClass = 'btn btn-primary edit-listing'
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
    sellModal.modal({backdrop: true});
})


// When user fills out form and clicks on button to submit, send POST request to 
// server to create or edit ListedGame in database depending on the button class
listingForm.submit((event) => {
    event.preventDefault();
    const data = createListingFormData();
    if ($('#user-list-button').hasClass('create-listing')) {
        createListing(data);
    } else if ($('#user-list-button').hasClass('edit-listing')) {
        editListing(data);
    }
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


