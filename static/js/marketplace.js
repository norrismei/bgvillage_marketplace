"use strict";

const listingsTable = $('#listings-results');

function displayListings(search_terms) {
    $.get('/api/marketplace.json', {"search_terms": `${search_terms}`}, (response) => {
        $('.listing-row').remove();
        for (const game of response) {
            listingsTable.append(
                `<tr class="listing-row" data-listing-id=${game.key} >
                    <td><img src=${game.image_url} height="50" /></td>
                    <td class="game-name">${game.name}</td>
                    <td>${game.condition}</td>
                    <td>$${game.price}</td>
                    <td class="seller-username" 
                        data-username=${game.username}>${game.username}</td>
                    <td><button class="email-seller">Email</button></td>
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


// Event handler for Email contact button
listingsTable.on('click', '.email-seller', (event) => {
    const listing = $(event.target);
    const game = listing.parent().siblings('.game-name').html();
    const seller = listing.parent().siblings('.seller-username').html();
    $.get('/api/user/email.json', {'username': seller}, (response) => {
        // response action here
        document.location = `mailto:${response}?subject=${game}`;
    })
})


// <---------------------Event handler for modal------------------------>
const modal = $('.modal');
const close = $('.close');

// Retrieve listing details when user clicks on game name
listingsTable.on('click', '.game-name', (event) => {
    const listing = $(event.target);
    const listingId = listing.parents().attr('data-listing-id');
    $.get('/api/listing/details.json', {"listing_id": listingId}, (response) => {
        console.log(response);
    })
    modal.show();
})

close.on('click', (event) => {
    modal.hide();
})

// Non-working code to close modal window if clicking anywhere outside modal

modal.on('click', (event) => {
    console.log('Clicked on document');
    console.log(`Event target: ${event.target}`);
    if (event.target !== $('.modal-content')) {
        modal.hide();
    }
})
