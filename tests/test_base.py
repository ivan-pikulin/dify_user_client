import unittest
from dify_user_client.base import Credentials

class TestCredentials(unittest.TestCase):
    def test_credentials_initialization(self):
        """Test that credentials can be initialized with username and password."""
        username = "test_user"
        password = "test_password"
        credentials = Credentials(username=username, password=password)
        self.assertEqual(credentials.username, username)
        self.assertEqual(credentials.password, password)

if __name__ == "__main__":
    unittest.main()
