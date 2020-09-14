"use strict";

const listingsTable = $('#listings-results');

function displayListings(listings) {
    $('.listing-row').remove();
    for (const game of listings) {
        const wishlistClass = game.wishlist ? "wishlist-true" : "wishlist-false"
        const recClass = game.recommended ? "rec-true" : "rec-false"
        listingsTable.append(
            `<tr class="listing-row ${wishlistClass} ${recClass}" 
                 data-listing-id=${game.key}>
                <td class="align-middle d-flex justify-content-center"><img src=${game.image_url} height="50" /></td>
                <td class="game-name align-middle text-center">${game.name}</td>
                <td class="align-middle text-center">${game.condition}</td>
                <td class="align-middle text-center">$${game.price}</td>
                <td class="seller-username align-middle text-center" 
                    data-username=${game.username}>${game.username}</td>
                <td class="align-middle text-center">
                    <button type="button" class="btn email-seller">
                        <svg width="1.5em" height="1.5em" viewBox="0 0 16 16" class="bi bi-envelope" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd" d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2zm13 2.383l-4.758 2.855L15 11.114v-5.73zm-.034 6.878L9.271 8.82 8 9.583 6.728 8.82l-5.694 3.44A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.739zM1 11.114l4.758-2.876L1 5.383v5.73z"/>
                        </svg>
                    </button>
                </td>
            </tr>`
        );
    };
}

function displaySearchResults(searchTerms) {
    $.get('/api/marketplace.json', {"search_terms": `${searchTerms}`}, (response) => {
        displayListings(response.games);
        if (response.rec_criteria) {
            $('#view-rec').removeAttr('disabled');
            $('#rec-criteria').html(formatRecCriteria(response.rec_criteria));
        };
    });
};

function displayAllListings() {
    $('#back-to-listings-search').hide();
    $('#rec-criteria').hide();
    displaySearchResults('');
} 

function formatRecCriteria(recCriteria) {
    const traits = recCriteria.join(', ');
    return `These games are recommended based on your interest in ${traits}.`
}

// Refreshing of displayed results upon submitting a search for a game
$('#listings-search-form').submit((event) => {
    event.preventDefault();
    const searchTerms = $('#listings-search-terms').val();
    displaySearchResults(searchTerms);
})

// Hiding/showing of listings dependent on view-selector choice
const viewOption = $('#view-selector');
viewOption.on('change', (event) => {
    if ($('#view-selector option:selected').attr('id') == "view-wishlist") {
        $('#rec-criteria').hide();
        $('.wishlist-false').hide();
        $('.wishlist-true').show();
    } else if ($('#view-selector option:selected').attr('id') == "view-rec") {
        $('#rec-criteria').show();
        $('.rec-false').hide();
        $('.rec-true').show();
    } else {
        $('#rec-criteria').hide();
        $('.listing-row').show();
    }
});


// Event handler for Email contact button
listingsTable.on('click', '.email-seller', (event) => {
    const listing = $(event.target);
    const game = listing.closest('td').siblings('.game-name').html();
    const seller = listing.closest('td').siblings('.seller-username').html();
    $.get('/api/user/email.json', {'username': seller}, (response) => {
        document.location = `mailto:${response}?subject=${game}`;
    })
})


// <---------------------Event handler for modal------------------------>
const modal = $('#listing-modal');
const modalBody = $('.modal-body');
const otherGames = $('#list-other-games');

// Retrieve listing details when user clicks on game name
listingsTable.on('click', '.game-name', (event) => {
    const listing = $(event.target);
    const listingId = listing.parents().attr('data-listing-id');
    const seller = listing.siblings('.seller-username').attr('data-username'); 
    const data = {"listing_id": listingId,
                  "username": seller}
    $.get('/api/listing/details.json', data, (response) => {
        $('#list-img').html(`<img src=${response.image_url} height="150" />`);
        $('#list-game-name').html(response.game_name);
        $('#list-condition').html(`<span class="list-label">Condition:</span> ${response.condition}`);
        $('#list-price').html(`<span class="list-label">Price:</span> ${response.price}`);
        if (response.msrp) {
            $('#list-msrp').html(`<span class="list-label">MSRP:</span> ${response.msrp}`);
        }
        $('#list-email').html(`
            <a href="mailto:${response.email}?subject=${response.game_name}">
                <button type="button" class="btn btn-outline-dark">
                    <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-envelope" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                      <path fill-rule="evenodd" d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2zm13 2.383l-4.758 2.855L15 11.114v-5.73zm-.034 6.878L9.271 8.82 8 9.583 6.728 8.82l-5.694 3.44A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.739zM1 11.114l4.758-2.876L1 5.383v5.73z"/>
                    </svg>
                    Email seller
                </button>
            </a>`)
        if (response.other_games) {
            $('#list-other-games').html(
                `<button type="button" class="btn btn-outline-dark view-other-games" data-username=${response.username}>
                    <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-person-lines-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                      <path fill-rule="evenodd" d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm7 1.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5zm0-3a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5zm2 9a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5z"/>
                    </svg>
                    View seller's listings
                </button>`);
        };
        if (response.comment) {
            $('#list-comment').html(`<span class="list-label">Comment:</span> ${response.comment}`);
        };
        if (response.min_age) {
            $('#list-min-age').html(`<span class="list-label">Min age:</span> ${response.min_age}`);
        };
        if (response.players) {
            $('#list-players').html(`<span class="list-label">Players:</span> ${response.players}`);
        };
        if (response.playtime) {
            $('#list-playtime').html(`<span class="list-label">Playtime:</span> ${response.playtime}`);
        };
        if (response.publisher) {
            $('#list-publisher').html(`<span class="list-label">Publisher:</span> ${response.publisher}`);
        };
        if (response.designers) {
            $('#list-designers').html(`<span class="list-label">Designers:</span> ${response.designers}`);
        };
        if (response.publish_year) {
            $('#list-year').html(`<span class="list-label">Year Published:</span> ${response.publish_year}`);
        };    
        if (response.game_description) {
            $('#list-description').html(`<span class="list-label">Description:</span><br>${response.game_description}`);
        }
        if (response.mechanics) {
            $('#list-mechanics').html(`<span class="list-label">Mechanics:</span> ${response.mechanics}`);
        };
        if (response.categories) {
            $('#list-categories').html(`<span class="list-label">Categories:</span> ${response.categories}`);
        };
        modal.modal({backdrop: true});
    })
})

// Links to Marketplace listings filtered by username when button is clicked
otherGames.on('click', '.view-other-games', (event) => {
    const username = $('.view-other-games').attr('data-username');
    $.get(`/api/marketplace/${username}.json`,response => {
            modal.modal('hide');
            $('.listings-search-field').hide();
            $('#back-to-listings-search').show();
            $('#rec-criteria').hide();
            $('#rec-criteria').html(formatRecCriteria(response.rec_criteria));
            $('#view-selector option:first').prop('selected', true);
            displayListings(response.games);
        })
})

// <------------------End of functions related to modal--------------------->


// From filtered user listings view, toggles back to all listings
$('#back-to-listings-search').on('click', 'button', (event) => {
    $('.listings-search-field').show();
    $('#back-to-listings-search').hide();
    $('#rec-criteria').hide();
    $('#view-selector option:first').prop('selected', true);
    displayAllListings();
}) 

// Initial loading of all Marketplace listings.
displayAllListings()
