import unittest

from server import app
from model import db, connect_to_db, create_example_data

class LoginTests(unittest.TestCase):
    """Tests for login page"""

    def setUp(self):
        """Steps to take before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        create_example_data()

    def tearDown(self):
        """Steps to take after every test"""

        db.session.close()
        db.drop_all()

    def test_no_existing_user(self):
        """Test login where no account exists for given username"""

        result = self.client.post("/handle-login",
                                  data={"username": "curtis", 
                                        "password": "gloomhaven"},
                                  follow_redirects=True)

        self.assertIn(b"No account with this username", result.data)
        self.assertNotIn(b"Board Game Shelf", result.data)

    def test_wrong_password(self):
        """Test login where wrong password given for existing username"""

        result = self.client.post("/handle-login",
                                  data={"username": "thodas", 
                                        "password": "gloomhaven"},
                                  follow_redirects=True)

        self.assertIn(b"Wrong password", result.data)
        self.assertNotIn(b"Board Game Shelf", result.data)

    def test_correct_login(self):
        """Test login where username and password are correct"""

        result = self.client.post("/handle-login",
                                  data={"username": "noramp", 
                                        "password": "gloomhaven"},
                                  follow_redirects=True)

        self.assertIn(b"Board Game Shelf", result.data)
        self.assertNotIn(b'placeholder="enter password"', result.data)


class UserPageTests(unittest.TestCase):
    """Tests that require user to be logged in to view their user page"""

    def setUp(self):
        """Steps to take before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'supersecret'

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        create_example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = 'thodas'
                sess['current_user_id'] = 2

    def tearDown(self):
        """Steps to take after every test"""

        with self.client as c:
            with c.session_transaction() as sess:
                del sess['current_user']
                del sess['current_user_id']

        db.session.close()
        db.drop_all()

    def test_user_page(self):
        """Test user can view their page when logged in"""

        result = self.client.get("/api/user/own-games.json")
        self.assertIn(b'"name":"1800"', result.data)


if __name__ == "__main__":
    unittest.main()

