import pytest

from dify_user_client import DifyClient
from dify_user_client.llms import ModelProvider, ModelProviderInfo


def test_model_providers(client: DifyClient):
    assert isinstance(client.model_providers, list)
    for model_provider in client.model_providers:
        assert isinstance(model_provider, ModelProvider)

    model_provider = client.get_model_provider("openai")
    assert isinstance(model_provider, ModelProvider)
    info = model_provider.info
    assert info.provider == "openai"
    assert isinstance(info, ModelProviderInfo)
