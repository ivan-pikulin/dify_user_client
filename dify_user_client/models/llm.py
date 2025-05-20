from typing import Optional, Union, Dict
from enum import Enum

from .base import BaseModel

class SupportedModelType(str, Enum):
    TEXT_EMBEDDING = "text-embedding"
    SPEECH2TEXT = "speech2text"
    MODERATION = "moderation"
    TTS = "tts"
    LLM = "llm"
    RERANK = "rerank"

class ModelProviderHelp(BaseModel):
    title: Union[Dict, str]
    url: Union[Dict, str]

class ModelProviderInfo(BaseModel):
    provider: str
    label: Optional[Union[Dict, str]] = None
    description: Optional[Union[Dict, str]] = None
    icon_small: Optional[Union[Dict, str]] = None
    icon_large: Optional[Union[Dict, str]] = None
    background: Optional[str] = None
    help: Optional[ModelProviderHelp] = None
    supported_model_types: list[SupportedModelType]
    configurate_methods: Optional[list[str]] = None
    provider_credential_schema: Optional[Dict] = None
    model_credential_schema: Optional[Dict] = None
    preferred_provider_type: Optional[str] = None
    custom_configuration: Optional[Dict] = None
    system_configuration: Optional[Dict] = None 