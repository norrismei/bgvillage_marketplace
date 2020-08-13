"""Models for Board Game Village Marketplace app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///bgvillage', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class User(db.Model):
    """A user"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date)

    user_game = db.relationship('UserGame', backref='users')
    wanted_game = db.relationship('WantedGame', backref='users')
    rating = db.relationship('Rating', backref='users')

    def __repr__(self):
        """Show human-readable info about user"""

        return f"<User id={self.id} username={self.username}>"


class Game(db.Model):
    """A game entity"""

    __tablename__ = "games"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    publish_year = db.Column(db.Integer)
    min_age = db.Column(db.Integer)
    min_players = db.Column(db.Integer)
    max_players = db.Column(db.Integer)
    min_playtime = db.Column(db.Integer)
    max_playtime = db.Column(db.Integer)
    image_url = db.Column(db.String)
    msrp = db.Column(db.Float)

    user_game = db.relationship('UserGame', backref='games')
    wanted_game = db.relationship('WantedGame', backref='games')
    rating = db.relationship('Rating', backref='games')
    game_mech = db.relationship('GameMechanic', backref='games')
    game_cat = db.relationship('GameCategory', backref='games')
    game_pub = db.relationship('GamePublisher', backref='games')
    game_design = db.relationship('GameDesigner', backref='games')
    game_art = db.relationship('GameArtist', backref='games')

    def __repr__(self):
        """Show human-readable info about game"""

        return f"<Game id={self.id} name={self.name}>"


class UserGame(db.Model):
    """A physical instance of a game owned by user"""

    __tablename__ = "user_games"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    own = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref='user_games')
    game = db.relationship('Game', backref='user_games')

    def __repr__(self):
        """Show human-readable UserGame instance"""

        return f"<UserGame id={self.id} "\
               f"user={self.user.username} game={self.game.name}>"


class WantedGame(db.Model):
    """A physical instance of a game wanted by user"""

    __tablename__ = "wanted_games"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    want_level = db.Column(db.String, nullable=False)
    comment = db.Column(db.String)

    user = db.relationship('User', backref='wanted_games')
    game = db.relationship('Game', backref='wanted_games')

    def __repr__(self):
        """Show human-readable WantedGame instance"""

        return f"<WantedGame id={self.id} "\
               f"user={self.user.username} game={self.game.name}>"


class Rating(db.Model):
    """A rating of game by user"""

    __tablename__ = "ratings"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)

    user = db.relationship('User', backref='ratings')
    game = db.relationship('Game', backref='ratings')

    def __repr__(self):
        """Show human-readable rating"""

        return f"<Rating id={self.id} "\
               f"game={self.game.name} rating={self.rating}>"


class Mechanic(db.Model):
    """A gaming mechanic"""

    __tablename__ = "mechanics"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String, nullable=False)
    atlas_id = db.Column(db.String, unique=True)

    game_mech = db.relationship('GameMechanic', backref='mechanics')

    def __repr__(self):
        """Show human-readable mechanic"""

        return f"<Mechanic id={self.id} name={self.name}>"


class GameMechanic(db.Model):
    """Abstract: an instance of a game tagged with a mechanic"""

    __tablename__ = "games_mechanics"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    mechanic_id = db.Column(db.Integer, db.ForeignKey("mechanics.id"))

    mech = db.relationship('Mechanic', backref='games_mechanics')
    game = db.relationship('Game', backref='games_mechanics')

    def __repr__(self):
        """Show human-readable GameMechanic instance"""

        return f"<GameMechanic id={self.id} "\
               f"game={self.game.name} mech={self.mech.name}>"


class Category(db.Model):
    """A gaming category"""

    __tablename__ = "categories"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String, nullable=False)
    atlas_id = db.Column(db.String, unique=True)

    game_cat = db.relationship('GameCategory', backref='categories')

    def __repr__(self):
        """Show human-readable category"""

        return f"<Category id={self.id} name={self.name}>"


class GameCategory(db.Model):
    """Abstract: an instance of a game tagged with a category"""

    __tablename__ = "games_categories"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    cat = db.relationship('Category', backref='games_categories')
    game = db.relationship('Game', backref='games_categories')

    def __repr__(self):
        """Show human-readable GameMechanic instance"""

        return f"<GameCategory id={self.id} "\
               f"game={self.game.name} cat={self.cat.name}>"


class Publisher(db.Model):
    """A game publisher"""

    __tablename__ = "publishers"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Show human-readable publisher"""

        return f"<Publisher id={self.id} name={self.name}>"


class GamePublisher(db.Model):
    """Abstract: an instance of a game tagged with a publisher"""

    __tablename__ = "games_publishers"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    publisher_id = db.Column(db.Integer, db.ForeignKey("publishers.id"))

    pub = db.relationship('Publisher', backref='games_publishers')
    game = db.relationship('Game', backref='games_publishers')

    def __repr__(self):
        """Show human-readable GamePublisher instance"""

        return f"<GamePublisher id={self.id} "\
               f"game={self.game.name} pub={self.pub.name}>"


class Designer(db.Model):
    """A game designer"""

    __tablename__ = "designers"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Show human-readable designer"""

        return f"<Designer id={self.id} name={self.name}>"


class GameDesigner(db.Model):
    """Abstract: an instance of a game tagged with a designer"""

    __tablename__ = "games_designers"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    designer_id = db.Column(db.Integer, db.ForeignKey("designers.id"))

    designer = db.relationship('Designer', backref='games_designers')
    game = db.relationship('Game', backref='games_designers')

    def __repr__(self):
        """Show human-readable GameDesigner instance"""

        return f"<GameDesigner id={self.id} "\
               f"game={self.game.name} design={self.designer.name}>"


class Artist(db.Model):
    """A game artist"""

    __tablename__ = "artists"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Show human-readable artist"""

        return f"<Artist id={self.id} name={self.name}>"


class GameArtist(db.Model):
    """Abstract: an instance of a game tagged with a artist"""

    __tablename__ = "games_artists"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))

    artist = db.relationship('Artist', backref='games_artists')
    game = db.relationship('Game', backref='games_artists')

    def __repr__(self):
        """Show human-readable GameArtist instance"""

        return f"<GameArtist id={self.id} "\
               f"game={self.game.name} art={self.artist.name}>"


if __name__ == '__main__':
    from server import app

    connect_to_db(app)