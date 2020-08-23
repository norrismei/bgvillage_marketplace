"use strict";

const listingsTable = $('#listings-results');

function displayListings(search_terms) {
    $.get('/api/marketplace.json', {"search_terms": `${search_terms}`}, (response) => {
        $('.listing-row').remove();
        for (const game of response) {
            listingsTable.append(
                `<tr class="listing-row">
                    <td><img src=${game.image_url} height="50" /></td>
                    <td>${game.name}</td>
                    <td>${game.condition}</td>
                    <td>$${game.price}</td>
                    <td>${game.username}</td>
                    <td><button>Email</button></td>
                </tr>`
            );
        }
    });
};

// Initial loading of all Marketplace listings. 
displayListings('');


// Refreshing of displayed results upon submitting a search for a game
$('#listings-search-form').submit((event) => {
    event.preventDefault();
    const searchTerms = $('#listings-search-terms').val();
    displayListings(searchTerms);
})
