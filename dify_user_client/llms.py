from enum import Enum
from typing import Literal, Optional, Union

from pydantic import BaseModel

from .base import DifyBaseClient


class ModelProviderHelp(BaseModel):
    title: Union[dict, str]
    url: Union[dict, str]


class SupportedModelType(str, Enum):
    text_embedding = "text-embedding"
    speech2text = "speech2text"
    moderation = "moderation"
    tts = "tts"
    llm = "llm"
    rerank = "rerank"


class ModelProviderInfo(BaseModel):
    provider: str
    label: Optional[Union[dict, str]] = None
    description: Optional[Union[dict, str]] = None
    icon_small: Optional[Union[dict, str]] = None
    icon_large: Optional[Union[dict, str]] = None
    background: Optional[str] = None
    help: Optional[ModelProviderHelp] = None
    supported_model_types: list[SupportedModelType]
    configurate_methods: Optional[list[str]] = None
    provider_credential_schema: Optional[dict] = None
    model_credential_schema: Optional[dict] = None
    preferred_provider_type: Optional[Literal["predefined", "custom"]] = None
    custom_configuration: Optional[dict] = None
    system_configuration: Optional[dict] = None


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
