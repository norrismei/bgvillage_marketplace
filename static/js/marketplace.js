"use strict";

const listingsTable = $('#listings-results');

function displayListings() {
    $.get('/api/marketplace.json', (response) => {
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

displayListings();