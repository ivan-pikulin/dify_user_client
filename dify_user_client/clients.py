import logging
from typing import Literal

import yaml

from .apps import App, AppType, WorkflowDraft
from .base import Credentials, DifyBaseClient
from .knowledge import DifyKnowledgeClient
from .llms import ModelProvider
from .models import ModelProviderInfo
from .tools import Tool, ToolProvider

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dify")


class DifyUserClient(DifyBaseClient):
    def update_timezone(self, timezone="Europe/Moscow"):
        url = f"{self.base_url}/console/api/account/timezone"
        body = {"timezone": timezone}
        self._send_user_request("POST", url, json=body)

    def update_system_model(self, model_settings: list[dict]):
        url = f"{self.base_url}/console/api/workspaces/current/default-model"
        self._send_user_request(
            "POST", url, json={"model_settings": model_settings})

    @property
    def _apps_mapping(self) -> dict[str, App]:
        def get_apps_page(page: int):
            url = f"{self.base_url}/console/api/apps"
            params = {
                "page": page,
                "limit": 100,
            }
            response = self._send_user_request("GET", url, params=params)
            apps = {
                app["id"]: App.create(
                    self, app["id"], mode=AppType(app["mode"]))
                for app in response["data"]
            }
            return apps, response["has_more"]

        i = 1
        apps = {}
        while True:
            new_apps, has_more = get_apps_page(i)
            apps.update(new_apps)
            i += 1
            if not has_more:
                break
        return apps

    @property
    def apps(self) -> list[App]:
        return list(self._apps_mapping.values())

    def get_app(self, app_id: str) -> App:
        try:
            return self._apps_mapping[app_id]
        except KeyError:
            raise ValueError(f"App with id {app_id} not found")

    @property
    def _tool_providers_mapping(self) -> dict[str, ToolProvider]:
        url = f"{self.base_url}/console/api/workspaces/current/tool-providers"
        response = self._send_user_request("GET", url)
        tool_providers = {
            provider["id"]: ToolProvider.create(
                self, provider["id"], type=provider["type"])
            for provider in response
        }
        return tool_providers

    @property
    def tool_providers(self) -> list[ToolProvider]:
        return list(self._tool_providers_mapping.values())

    def get_tool_provider(self, provider_id: str) -> ToolProvider:
        return self._tool_providers_mapping[provider_id]

    @property
    def tools(self) -> list[Tool]:
        tools = []
        for provider in self.tool_providers:
            tools.extend(provider.tools)
        return tools

    def get_tool(self, name: str) -> Tool:
        for tool in self.tools:
            if tool.name == name:
                return tool
        raise ValueError(f"Tool with name {name} not found")

    def __fetch_model_providers_info(self) -> list[ModelProviderInfo]:
        url = f"{self.base_url}/console/api/workspaces/current/model-providers"
        response = self._send_user_request("GET", url)["data"]
        return [ModelProviderInfo(**provider) for provider in response]

    @property
    def _model_provider_info_mapping(self) -> dict[str, ModelProviderInfo]:
        return {
            provider.provider: provider for provider in self.__fetch_model_providers_info()
        }

    @property
    def _model_providers_mapping(self):
        model_providers_info = self.__fetch_model_providers_info()
        model_providers = {
            provider.provider: ModelProvider(self, provider.provider) for provider in model_providers_info
        }
        return model_providers

    @property
    def model_providers(self) -> list[ModelProvider]:
        return list(self._model_providers_mapping.values())

    def get_model_provider(self, provider_id: str) -> ModelProvider:
        try:
            return self._model_providers_mapping[provider_id]
        except KeyError:
            raise ValueError(f"Model provider with id {provider_id} not found")

    def create_app(self, name: str, mode: AppType,
                   description: str = "", icon_type: Literal["emoji", "image"] = "emoji",
                   icon: str = "🤖", icon_background: str = "#FFEAD5") -> App:
        url = f"{self.base_url}/console/api/apps"
        body = {
            "name": name,
            "mode": mode,
            "description": description,
            "icon_type": icon_type,
            "icon": icon,
            "icon_background": icon_background,
        }
        response = self._send_user_request("POST", url, json=body)
        app = App.create(client=self, id=response["id"], mode=mode)
        if mode == AppType.workflow or mode == AppType.advanced_chat:
            app.update_draft(draft=WorkflowDraft())
        return app

    def create_app_from_yaml(self, yaml_content: str) -> App:
        url = f"{self.base_url}/console/api/apps/imports"
        body = {
            "mode": "yaml-content",
            "yaml_content": yaml_content,
        }
        response = self._send_user_request("POST", url, json=body)
        mode = AppType(yaml.safe_load(yaml_content)["app"]["mode"])
        return App.create(client=self, id=response["app_id"], mode=mode)

    def delete_app(self, app_id: str) -> None:
        url = f"{self.base_url}/console/api/apps/{app_id}"
        self._send_user_request("DELETE", url)


class DifyClient(DifyUserClient):
    def __init__(self, base_url: str, credentials: Credentials):
        super().__init__(base_url, credentials)
        self.knowledge = DifyKnowledgeClient(base_url, credentials)
