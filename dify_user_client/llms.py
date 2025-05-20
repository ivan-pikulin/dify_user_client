from enum import Enum
from typing import Union

from pydantic import BaseModel

from .base import DifyBaseClient
from .models import ModelProviderInfo


class ModelProviderHelp(BaseModel):
    title: Union[dict, str]
    url: Union[dict, str]


class ModelProvider:
    def __init__(self, client: 'DifyBaseClient', id: str):
        self.client = client
        self.id = id

    @property
    def info(self) -> ModelProviderInfo:
        return self.client._model_provider_info_mapping[self.id]

    def update_credentials(self, credentials: dict):
        url = f"{self.client.base_url}/console/api/workspaces/current/model-providers/{self.id}"
        body = {"credentials": credentials}
        self.client._send_user_request("POST", url, json=body)

    def validate_credentials(self, credentials: dict):
        url = f"{self.client.base_url}/console/api/workspaces/current/model-providers/{self.id}/credentials/validate"
        body = {"credentials": credentials}
        self.client._send_user_request("POST", url, json=body)

    def delete(self):
        url = f"{self.client.base_url}/console/api/workspaces/current/model-providers/{self.id}"
        self.client._send_user_request("DELETE", url)
