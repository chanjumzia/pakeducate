
import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index(self):
        """Test the index page."""
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b"Welcome to the School Management System!", rv.data)

if __name__ == "__main__":
    unittest.main()
