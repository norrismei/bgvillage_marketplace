$('#games-results').html(
    `<th>Add</th>
     <th>Image</th>
     <th>Name</th>
     <th>Players</th>
     <th>Publisher</th>`
);
$.get('/api/games.json', (response) => {
    for (const game of response) {
        let players = [];
            if (game.min_players) {
                players = `${game.min_players}`;
                if (game.max_players && 
                    game.max_players != game.min_players) {
                    players = `${game.min_players}-${game.max_players}`
                };
            };
        $('#games-results').append(
            `<tr>
                <td>
                    <button class="add-game" 
                            data-game-id="${game.key}">
                        Add Game
                    </button>
                </td>
                <td><img src=${game.image_url} height="50" /></td>
                <td>${game.name}</td>
                <td>${players}</td>
                <td>${game.publisher}</td>
            </tr>`
        );
    };
  });

// An example of event delegation. If we selected the buttons, which are
// dynamically produced, the event handler won't bind to them. Instead, select
// the parent element and move the button selector to second parameter of .on()
// method.
$('#games-results').on('click', 'button', (event) => {
    const addButton = $(event.target);
    const addButtonId = addButton.attr('data-game-id');
    $.post('/api/add-game', {'game_id': addButtonId}, (res) => {
        alert(res);
    });
})
