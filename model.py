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

    game_mech = db.relationship('GameMechanic', backref='games')
    game_cat = db.relationship('GameCategory', backref='games')

    def __repr__(self):
        """Show human-readable info about game"""

        return f"<Game id={self.id} name={self.name}>"


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


if __name__ == '__main__':
    from server import app

    connect_to_db(app)