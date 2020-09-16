# <img src="https://github.com/norrismei/bgvillage_marketplace/blob/master/static/img/board_game_village_meeple.jpeg" width="50%" alt="Board Game Village">
Welcome to Board Game Village, where the long-term vision is to connect players and encourage more playing of games in real life. On the user home page, users can keep track of their board game collection and wishlist by searching and adding games from the Board Game Atlas API to their virtual board game shelves, and easily create listings for games they want to sell. In the Marketplace, users can see all listings or get a personalized view of wishlist matches and recommended games. The app uses an original algorithm to analyze each user’s board game collection and wishlist for trends in game mechanics and categories to generate the recommendations.

## About Me
When I first learned Python, I discovered coding was not unlike learning the rules and strategy to a game, solving escape room puzzles, and editing — all activities that I enjoy. I doubled down on my decision to switch careers by attending Hackbright Academy, a full-stack software engineering program with a mission to #changetheratio in tech. I'm thrilled to combine my skills, talent, and interests into my new path as a software engineer.

## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Future Development](#future)

## <a name="tech-stack"></a>Tech Stack
* Python
* Flask
* Jinja2
* Javascript
* jQuery
* PostgreSQL
* SQLAlchemy ORM
* HTML
* CSS
* Bootstrap

## <a name="features"></a>Features

![alt text](https://github.com/norrismei/bgvillage_marketplace/blob/master/static/img/user_page_toggle.gif "Toggling Board Game Shelf views")

#### Board Game Shelf
In Board Game Village, each user has a Shelf to keep track of games they own, games for sale, and games they wish to buy. Using Javascript, I added event handlers that listen for a click on the buttons. They make an AJAX call to a server route, which is set up using Flask as the web framework and written in Python. The route makes a query to my database using SQLAlchemy ORM, and returns the data in JSON. The result is the page can quickly update the parts that have changed without reloading the whole page.

![alt text](https://github.com/norrismei/bgvillage_marketplace/blob/master/static/img/add_game.gif "Adding game to Wishlist")

#### Add Games
To add games to the Board Game Shelf, users can search for a game by name. A call is made to a server route that makes a request to the <a href="https://www.boardgameatlas.com/api/docs">Board Game Atlas API</a>. It can take a few moments to get the response, so I included a loader icon. When I decide to add agame, another request is made to the server to check if the game details already exist in the database. If not, it’ll get it from the API to store. I decided to do it this way because I wanted users to be able to search all games, but I didn’t want to waste space storing data about games that no one’s doing anything.

![alt text](https://github.com/norrismei/bgvillage_marketplace/blob/master/static/img/create_listing.gif "Creating game listing")

#### Create/Edit Listing
Users can choose from a dropdown which of their owned games to list for sale. A modal will open for the user to input the game's condition and price and an optional comment. Once listed, a game listing can be edited or if the user changes their mind and wants to keep the game, they can remove the listing. If a game is sold, the user should remove the game from their collection, which will also remove the listing.

![alt text](https://github.com/norrismei/bgvillage_marketplace/blob/master/static/img/create_listing.gif "Creating game listing")

#### Find Wishlist Matches and Recommended Games
In the Marketplace, user can see all games being sold and filter to see only ones matching their wishlist or listings for recommended games. To recommend games, the app's algorithm analyzes the games the user owns or wishes to own, finds the top three mechanics and categories for a total of 6 traits, and finds matches in the marketplace that have at least one of these traits, not including any games the user already owns or wishes to own. The matched traits are shown along with the results. 

## <a name="future"></a>Future Development