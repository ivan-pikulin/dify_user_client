
from pydantic import BaseModel
import requests


class Credentials(BaseModel):
    username: str
    password: str


class DifyBaseClient:
    def __init__(self, base_url: str, credentials: Credentials):
        self.base_url = base_url
        self.credentials = credentials
        self._login()

    def _login(self):
        url = f"{self.base_url}/console/api/login"
        body = {
            "email": self.credentials.username,
            "password": self.credentials.password,
            "language": "ru-RU",
            "remember_me": True
        }

        response = requests.post(url, json=body)
        if response.status_code == 200:
            result = response.json()
            if result.get("result") == "success":
                self.access_token = result["data"]["access_token"]
                self.refresh_token = result["data"]["refresh_token"]
            else:
                raise ValueError(
                    f"Failed to log in: Invalid credentials or server error. Response: {response.text}")
        else:
            raise ValueError(
                f"Failed to log in: Server returned an error. Status code: {response.status_code}, Response: {response.text}")

    def _send_user_request(self, method: str, url: str, **kwargs):
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"

        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code == 401:
            self._login()
            return self._send_user_request(method, url, headers=headers, **kwargs)
        if response.status_code not in (200, 201, 204):
            raise ValueError(
                f"Request failed: {response.status_code} - {response.text}")
        if method == "DELETE":
            return None
        else:
            return response.json()
