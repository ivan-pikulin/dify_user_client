import requests
from datetime import datetime, timedelta
from typing import Optional
from .models.base import BaseModel


class Credentials(BaseModel):
    username: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: Optional[datetime] = None


class DifyBaseClient:
    def __init__(self, base_url: str, credentials: Credentials):
        self.base_url = base_url
        self.credentials = credentials
        self._token_info: Optional[TokenInfo] = None
        self._login()

    def _login(self):
        url = f"{self.base_url}/console/api/login"
        body = {
            "email": self.credentials.username,
            "password": self.credentials.password,
            "language": "ru-RU",
            "remember_me": True
        }

        try:
            response = requests.post(url, json=body)
            response.raise_for_status()
            result = response.json()
            
            if result.get("result") != "success":
                raise ValueError(f"Login failed: {result.get('message', 'Unknown error')}")
            
            # Store token info with expiration time (assuming 1 hour validity)
            self._token_info = TokenInfo(
                access_token=result["data"]["access_token"],
                refresh_token=result["data"]["refresh_token"],
                expires_at=datetime.now() + timedelta(hours=1)
            )
        except requests.RequestException as e:
            raise ValueError(f"Failed to log in: {str(e)}") from e

    def _refresh_token(self):
        if not self._token_info or not self._token_info.refresh_token:
            self._login()
            return

        url = f"{self.base_url}/console/api/refresh"
        headers = {"Authorization": f"Bearer {self._token_info.refresh_token}"}

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("result") != "success":
                self._login()
                return

            # Update token info with new tokens
            self._token_info.access_token = result["data"]["access_token"]
            self._token_info.refresh_token = result["data"]["refresh_token"]
            self._token_info.expires_at = datetime.now() + timedelta(hours=1)
        except requests.RequestException:
            self._login()

    def _ensure_valid_token(self):
        if not self._token_info:
            self._login()
            return

        # Refresh token if it's expired or about to expire in the next 5 minutes
        if not self._token_info.expires_at or \
           datetime.now() + timedelta(minutes=5) >= self._token_info.expires_at:
            self._refresh_token()

    def _send_user_request(self, method: str, url: str, **kwargs):
        self._ensure_valid_token()
        
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self._token_info.access_token}"
        kwargs["headers"] = headers

        try:
            response = requests.request(method, url, **kwargs)
            
            if response.status_code == 401:
                # Token might be invalid, try refreshing
                self._refresh_token()
                headers["Authorization"] = f"Bearer {self._token_info.access_token}"
                response = requests.request(method, url, **kwargs)
            
            response.raise_for_status()
            
            if method == "DELETE":
                return None
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Request failed: {str(e)}") from e
