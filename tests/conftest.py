import pytest
import os
from dotenv import load_dotenv
from dify_user_client import DifyClient
from dify_user_client.base import Credentials

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def client():
    return DifyClient(
        base_url=os.getenv("DIFY_BASE_URL"),
        credentials=Credentials(
            username=os.getenv("DIFY_USERNAME"),
            password=os.getenv("DIFY_PASSWORD")
        )
    )
