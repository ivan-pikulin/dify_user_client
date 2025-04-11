import unittest
from unittest.mock import patch, MagicMock, call
from dify_user_client.clients import DifyClient
from dify_user_client.base import Credentials

class TestDifyClient(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://api.dify.ai"
        self.credentials = Credentials(username="test_user", password="test_password")
    
    @patch('requests.request')
    @patch('requests.post')
    def test_get_applications(self, mock_post, mock_request):
        """Test that apps property returns the expected data."""
        # Mock the login response
        mock_login_response = MagicMock()
        mock_login_response.status_code = 200
        mock_login_response.json.return_value = {
            "result": "success",
            "data": {
                "access_token": "test_token",
                "refresh_token": "test_refresh_token"
            }
        }
        mock_post.return_value = mock_login_response

        # Mock the apps response
        mock_apps_response = MagicMock()
        mock_apps_response.json.return_value = {
            "data": [{"id": "1", "name": "Test App", "mode": "chat"}],
            "has_more": False
        }
        mock_apps_response.status_code = 200
        mock_request.return_value = mock_apps_response
        
        # Create client (this will trigger the login)
        self.client = DifyClient(base_url=self.base_url, credentials=self.credentials)
        
        # Call the method
        result = self.client.apps
        
        # Assert the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "1")
        
        # Assert the requests were made correctly
        expected_login_call = call(
            f"{self.base_url}/console/api/login",
            json={
                "email": "test_user",
                "password": "test_password",
                "language": "ru-RU",
                "remember_me": True
            }
        )
        mock_post.assert_has_calls([expected_login_call])
        
        expected_apps_call = call(
            "GET",
            f"{self.base_url}/console/api/apps",
            headers={"Authorization": "Bearer test_token"},
            params={"page": 1, "limit": 100}
        )
        mock_request.assert_has_calls([expected_apps_call])

if __name__ == "__main__":
    unittest.main() 