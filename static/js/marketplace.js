"use strict";

const listingsTable = $('#listings-results');

function displayListings() {
    $.get('/api/marketplace.json', (response) => {
        // row rendering here
    }
}