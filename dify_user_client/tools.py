import warnings
from typing import Literal, Union, Optional, Any

from pydantic import BaseModel

from .base import DifyBaseClient
from .models import (
    ToolInfo, ToolParameter, ToolParameterOption, WorkflowToolProviderInfo,
    Icon, WorkflowToolParameter
)


class ToolParameterOption(BaseModel):
    value: str
    label: Union[dict, str]


class ToolParameter(BaseModel):
    name: str
    label: Union[dict, str]
    human_description: Optional[Union[dict, str]] = None
    placeholder: Optional[Union[dict, str]] = None
    type: Literal["string", "number", "boolean",
                  "select", "file", "files", "secret-input"]
    form: Literal["llm", "form"]
    llm_description: Optional[str] = None
    required: bool
    default: Optional[Any] = None
    min: Optional[float] = None
    max: Optional[float] = None
    options: Optional[list[ToolParameterOption]] = None


class ToolInfo(BaseModel):
    author: str
    name: str
    label: Union[dict, str]
    description: Union[dict, str]
    parameters: list[ToolParameter]
    labels: list[str]


class Icon(BaseModel):
    content: str
    background: str


class WorkflowToolParameter(BaseModel):
    name: str
    description: str
    form: Literal["llm", "form"]


class WorkflowToolProviderInfo(BaseModel):
    name: str
    label: str
    workflow_tool_id: Optional[str] = None
    workflow_app_id: str
    icon: Icon
    description: str
    parameters: list[WorkflowToolParameter]
    tool: ToolInfo


class ToolProvider:
    type = None

    def __init__(self, client: 'DifyBaseClient', id: str):
        self.id = id
        self.client = client

    @classmethod
    def create(cls, client: 'DifyBaseClient', id: str, type: Literal["workflow", "builtin"]) -> 'ToolProvider':
        if type == "workflow":
            return WorkflowToolProvider(client=client, id=id)
        elif type == "builtin":
            return BuiltinToolProvider(client=client, id=id)
        else:
            warnings.warn(f"Invalid tool provider type: {type}", UserWarning)
            return ToolProvider(client=client, id=id)

    @property
    def tool_info(self):
        raise NotImplementedError(
            "info is not implemented for this tool provider")


class WorkflowToolProvider(ToolProvider):
    type = "workflow"

    @property
    def info(self) -> WorkflowToolProviderInfo:
        url = f"{self.client.base_url}/console/api/workspaces/current/tool-provider/workflow/get"
        params = {"workflow_tool_id": self.id}
        response = self.client._send_user_request("GET", url, params=params)
        return WorkflowToolProviderInfo(**response)

    @property
    def tools(self):
        return [WorkflowTool(
            client=self.client,
            provider=self,
            name=self.info.workflow_tool_id
        )]


class BuiltinToolProvider(ToolProvider):
    type = "builtin"

    @property
    def tools(self) -> list['BuiltinTool']:
        url = f"{self.client.base_url}/console/api/workspaces/current/tool-provider/builtin/{self.id}/tools"
        response = self.client._send_user_request("GET", url)
        return [BuiltinTool(
            client=self.client,
            provider=self,
            name=tool["name"]
        ) for tool in response]

    @property
    def tools_info(self) -> dict[str, ToolInfo]:
        url = f"{self.client.base_url}/console/api/workspaces/current/tool-provider/builtin/{self.id}/tools"
        response = self.client._send_user_request("GET", url)
        return {tool["name"]: ToolInfo(**tool) for tool in response}

    def update_credentials(self, credentials: dict):
        url = f"{self.client.base_url}/console/api/workspaces/current/tool-provider/builtin/{self.id}/update"
        body = {"credentials": credentials}
        self.client._send_user_request("POST", url, json=body)


class Tool:
    def __init__(self, client: 'DifyBaseClient', provider: ToolProvider, name: str):
        self.client = client
        self.provider = provider
        self.name = name

    @classmethod
    def create(cls, client: 'DifyBaseClient', provider: ToolProvider, name: str, mode: Literal["workflow", "builtin"]) -> 'Tool':
        if mode == "workflow":
            return WorkflowTool(client=client, provider=provider, name=name)
        elif mode == "builtin":
            return BuiltinTool(client=client, provider=provider, name=name)
        else:
            raise ValueError(f"Invalid tool mode: {mode}")

    @property
    def info(self) -> ToolInfo:
        raise NotImplementedError("info is not implemented for this tool")


class WorkflowTool(Tool):
    @property
    def workflow_app_id(self) -> str:
        return self.info.workflow_app_id

    @property
    def info(self) -> ToolInfo:
        return self.provider.info.tool


class BuiltinTool(Tool):
    @property
    def info(self) -> ToolInfo:
        url = f"{self.client.base_url}/console/api/workspaces/current/tool-provider/builtin/{self.id}/tools"
        response = self.client._send_user_request("GET", url)
        return ToolInfo(**response)

    @property
    def info(self) -> ToolInfo:
        return self.provider.tools_info[self.name]
