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
                <td><button class="add-game">Add Game</button></td>
                <td><img src=${game.image_url} height="50" /></td>
                <td>${game.name}</td>
                <td>${players}</td>
                <td>${game.publisher}</td>
            </tr>`
        );
    };
  });
