import unittest
from unittest.mock import patch, MagicMock, call
from dify_user_client.knowledge import DifyKnowledgeClient, KnowledgeDataset, KnowledgeDocument, DocumentData, DocumentIndexingStatuses, KnowledgeToken
from dify_user_client.base import Credentials

class TestKnowledgeDocument(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://stage.platform.abstergo.online"
        self.credentials = Credentials(username="test_user", password="test_password")
        self.dataset_id = "1319c144-b9fa-4cc5-99fd-fce69bbd5868"
        self.document_id = "d0aa351f-43a1-4d1c-ad8f-fc1a31666dc5"
        
        # Create mock client with mocked login
        with patch('requests.post') as mock_post:
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
            
            self.client = DifyKnowledgeClient(base_url=self.base_url, credentials=self.credentials)
            self.dataset = KnowledgeDataset(id=self.dataset_id, client=self.client)
            self.document = KnowledgeDocument(id=self.document_id, client=self.client, dataset=self.dataset)

    @patch('requests.request')
    def test_get_document_data(self, mock_request):
        """Test that document.data property returns the expected data."""
        # Mock the token response
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            "data": [{
                "id": "test_token_id",
                "type": "dataset",
                "token": "test_api_token",
                "created_at": 1234567890
            }]
        }
        mock_token_response.status_code = 200

        # Mock the document data response
        mock_doc_response = MagicMock()
        mock_doc_response.json.return_value = {
            "id": self.document_id,
            "dataset_id": self.dataset_id,
            "name": "Test Document",
            "content": "Test content",
            "created_at": 1234567890,
            "updated_at": 1234567890,
            "indexing_status": "completed",
            "word_count": 2,
            "character_count": 12,
            "segment_count": 1,
            "metadata": {"key": "value"}
        }
        mock_doc_response.status_code = 200

        # Set up the mock to return different responses for different calls
        mock_request.side_effect = [mock_token_response, mock_doc_response]

        # Call the method
        result = self.document.data

        # Assert the result
        self.assertIsInstance(result, DocumentData)
        self.assertEqual(result.id, self.document_id)
        self.assertEqual(result.dataset_id, self.dataset_id)
        self.assertEqual(result.name, "Test Document")
        self.assertEqual(result.content, "Test content")
        self.assertEqual(result.indexing_status, DocumentIndexingStatuses.COMPLETED)
        self.assertEqual(result.word_count, 2)
        self.assertEqual(result.character_count, 12)
        self.assertEqual(result.segment_count, 1)
        self.assertEqual(result.metadata, {"key": "value"})

        # Assert the requests were made correctly
        expected_token_call = call(
            "GET",
            f"{self.base_url}/console/api/datasets/api-keys",
            headers={"Authorization": "Bearer test_token"}
        )
        expected_doc_call = call(
            "GET",
            f"{self.base_url}/console/api/datasets/{self.dataset_id}/documents/{self.document_id}",
            headers={"Authorization": "Bearer test_api_token"},
            params={"metadata": "without"}
        )
        mock_request.assert_has_calls([expected_token_call, expected_doc_call])

if __name__ == "__main__":
    unittest.main() 