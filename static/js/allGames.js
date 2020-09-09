"use strict";

// Add rows of games retrieved from API underneath our table header
function addGameRows(games) {
    for (const game of games) {
        let players = [];
        if (game.min_players) {
            players = `${game.min_players}`;
            if (game.max_players && 
                game.max_players != game.min_players) {
                players = `${game.min_players}-${game.max_players}`
            };
        };
        $('#games-results').append(
            `<tr class="game-row">
                <td>
                    <div class="dropdown">
                        <button type="button" class="btn btn-outline-dark btn-sm dropdown-button" 
                                data-atlas-id="${game.key}">
                            <svg width=".75em" height=".75em" viewBox="0 0 16 16" class="bi bi-plus-circle" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                              <path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                              <path fill-rule="evenodd" d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                            </svg> 
                            Add Game
                        </button>
                        <div class="add-dropdown-content">
                            <div class="add-option add-to-own">to Own</div>
                            <div class="add-option add-to-wishlist">to Wishlist</div>
                        </div>
                    </div>
                </td>
                <td><img src=${game.image_url} height="50" /></td>
                <td>${game.name}</td>
                <td>${players}</td>
                <td>${game.publisher}</td>
            </tr>`
        );
    };
  };

// Initial loading of All Games page. Preloads with this search.
$.get('/api/games/search.json', {"search_terms": "%"}, (response) => {
    addGameRows(response);
    }
)


// Refreshing of displayed results upon submitting a search for a game
$('#games-search-form').submit((event) => {
    event.preventDefault();
    const searchTerms = $('#game-search-terms').val();
    $.get('/api/games/search.json', {"search_terms": searchTerms}, (response) => {
        $('.game-row').remove();
        addGameRows(response);
    })
})

// An example of event delegation. If we selected the buttons, which are
// dynamically produced, the event handler won't bind to them. Instead, select
// the parent element and move the button selector to second parameter of .on()
// method.

// Show drop-down menu when clicking on Add Game
$('#games-results').on('click', 'button', (event) => {
    const addButton = $(event.target);
    addButton.next("div").toggleClass("show");
})

// Handles the event, depending on which option user clicks
$('#games-results').on('click', '.add-option', (event) => {
    const addOption = $(event.target);
    const addAtlasId = addOption.parents('.add-dropdown-content').
                        siblings('.dropdown-button').attr('data-atlas-id');
    const addName = addOption.parents('.add-dropdown-content').
                        parents('.dropdown').parents('td').
                        siblings('.game-name').html();
    if (addOption.hasClass('add-to-own')) {
        $.post('/api/add-game', {'atlas_id': addAtlasId,
                                 'name': addName, 
                                 'add_type': 'own'}, (res) => {
            alert(res);
            // Close the open dropdown
            addOption.parents('.add-dropdown-content').toggleClass('show');
        });
    };
    if (addOption.hasClass('add-to-wishlist')) {
        $.post('/api/add-game', {'atlas_id': addAtlasId, 
                                 'name': addName,
                                 'add_type': 'wishlist'}, (res) => {
            alert(res);
            // Close the open dropdown
            addOption.parents('.add-dropdown-content').toggleClass('show');
        });
    };
})
