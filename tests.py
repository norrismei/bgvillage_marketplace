import unittest

from server import app
from model import db, connect_to_db, create_example_data

class FlaskTests(unittest.TestCase):
    """Tests for website app views"""

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


if __name__ == "__main__":
    unittest.main()

