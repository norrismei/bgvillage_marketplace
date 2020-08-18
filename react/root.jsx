"use strict";

const Router = ReactRouterDOM.BrowserRouter;
const Route =  ReactRouterDOM.Route;
const Link =  ReactRouterDOM.Link;
const Prompt =  ReactRouterDOM.Prompt;
const Switch = ReactRouterDOM.Switch;
const Redirect = ReactRouterDOM.Redirect;

function Homepage() {
    return <div> Welcome to Board Game Village </div>
}

function OwnGames() {

    const [ownGameList, setOwnGameList] = React.useState([])

    React.useEffect(() => {
        let mounted = true
        fetch('/api/own_games.json')
        .then((response) => response.json())
        .then((data) => {
            if (mounted) {
                setOwnGameList(data);
            };
        });
        return () => mounted = false
    }, []);

    const displayOwnGames = []

    for (const game of ownGameList) {
        displayOwnGames.push(
            <tr key={game.id}>
                <td></td>
                <td>{game.name}</td>
                <td>{game.min_players}-{game.max_players}</td>
                <td>{game.min_playtime}-{game.max_playtime} mins</td>
                <td></td>
            </tr>
        );
    }

    return (
        <React.Fragment>
            <table>
                <tbody>
                    <tr>
                        <th>Sell</th>
                        <th>Name</th>
                        <th>Players</th>
                        <th>Playtime</th>
                        <th>Remove</th>
                    </tr>
                    {displayOwnGames}
                </tbody>
            </table>
            <button>Add Game</button>
        </React.Fragment>
    );

};

function ListedGames() {

    const [listedGameList, setListedGameList] = React.useState([])

    React.useEffect(() => {
        let mounted = true
        fetch('/api/listed_games.json')
        .then((response) => response.json())
        .then((data) => {
            if (mounted) {
                setListedGameList(data);
            };
        });
        return () => mounted = false
    }, []);

    const displayListedGames = []

    for (const game of listedGameList) {
        displayListedGames.push(
            <li key={game.key}>{game.name}</li>
        );
    }

    // function handleClick {
    //     const newGame = 
    //     setListedGameList();
    // }

    return (
        <ul>
            {displayListedGames}
        </ul>
    );

}

function WantedGames() {

    const [wantedGameList, setWantedGameList] = React.useState([])

    React.useEffect(() => {
        let mounted = true
        fetch('/api/wanted_games.json')
        .then((response) => response.json())
        .then((data) => {
            if (mounted) {
                setWantedGameList(data);
            };
        });
        return () => mounted = false
    }, []);

    const displayWantedGames = []

    for (const game of wantedGameList) {
        displayWantedGames.push(
            <li key={game.key}>{game.name}</li>
        );
    }

    return (
        <React.Fragment>
            <ul>
                {displayWantedGames}
            </ul>
            <button>Add Game</button>
        </React.Fragment>
    );

}

function BoardGameShelfContainer() {

    const [gameList, setGameList] = React.useState(<OwnGames />);

    function showOwnGames() {
        setGameList(<OwnGames />)
    };

    function showSellGames() {
        setGameList(<ListedGames />)
    };

    function showWantedGames() {
        setGameList(<WantedGames />)
    };

    return (
        <React.Fragment>
            <h1>Board Game Shelf</h1>
            {/*Render the Add Game button*/}
            <button id="own-button" onClick={showOwnGames}>Own</button>
            <button id="sell-button" onClick={showSellGames}>Sell</button>
            <button id="wishlist-button" onClick={showWantedGames}>Wishlist</button>
            <div>
               {gameList}
            </div>
        </React.Fragment>
    );
}


function UserPage() {
    return (
        <React.Fragment>
            {/*Render the link to marketplace component*/}
            {/*Render the heading component*/}
            <BoardGameShelfContainer />
        </React.Fragment>
    );
}


function App() {
    return (
        <Router>
            <div>
                <ul>
                    <li>
                        <Link to="/"> Home </Link>
                    </li>
                    <li>
                        <Link to="/users/1"> My Games </Link>
                    </li>
                </ul>
                <Switch>
                    <Route path="/users/1">
                        <UserPage />
                    </Route>
                    <Route path="/">
                        <Homepage />
                    </Route>
                </Switch>
            </div>
        </Router>
      );
}

ReactDOM.render(<App />, document.getElementById('root'))