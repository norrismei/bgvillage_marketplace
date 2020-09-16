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

## <a name="future"></a>Future Development