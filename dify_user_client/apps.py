import warnings
from enum import Enum
from typing import Literal, Optional, Generator

from pydantic import BaseModel
import yaml

from .base import DifyBaseClient
from .tools import WorkflowToolProviderInfo
from .models import (
    AppType, AppToken, Graph, GraphNode, GraphEdge, GraphNodeData, GraphEdgeData, 
    Viewport, WorkflowDraft, PaginatedWorkflowLogs, PaginatedAgentLogs, 
    WorkflowLogEntry, AgentConversation, WorkflowNodeExecutions,
    PaginatedChatMessages
)


class AppType(str, Enum):
    workflow = "workflow"
    chat = "chat"
    advanced_chat = "advanced-chat"
    agent = "agent-chat"
    completion = "completion"


GraphNodeDataTypes = Literal["start", "end", "llm"]


class GraphNodeData(BaseModel):
    type: GraphNodeDataTypes
    title: str
    description: str
    variables: list


class GraphEdgeData(BaseModel):
    sourceType: GraphNodeDataTypes
    targetType: GraphNodeDataTypes
    isInIteration: bool


class GraphNode(BaseModel):
    id: str
    type: str
    data: dict
    position: dict
    targetPosition: str
    sourcePosition: str
    positionAbsolute: dict
    width: int
    height: int


class GraphEdge(BaseModel):
    id: str
    type: str
    source: str
    sourceHandle: str
    target: str
    targetHandle: str
    data: GraphEdgeData
    zIndex: int


class Viewport(BaseModel):
    x: Optional[int] = 0
    y: Optional[int] = 0
    zoom: Optional[int] = 1


class Graph(BaseModel):
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    viewport: Viewport = Viewport()


class WorkflowDraft(BaseModel):
    graph: Optional[Graph] = Graph()
    features: dict = {}
    environment_variables: list = []
    conversation_variables: list = []


class AppToken(BaseModel):
    id: str
    type: Literal["app"]
    token: str
    last_used_at: Optional[int] = None
    created_at: int


class Chat:
    def __init__(self, client: 'DifyBaseClient', app: 'App', id: str, info: dict = None):
        self.id = id
        self.app = app
        self.client = client
        self.info = info or {}

    @property
    def messages(self, max_pages=10):
        def fetch_messages(page=1):
            url = f"{self.client.base_url}/console/api/apps/{self.app.id}/chat-messages?conversation_id={self.id}&limit=10&page={page}"
            return self.client._send_user_request("GET", url)

        results = []
        page = 1
        while True:
            result = fetch_messages(page)
            results += result['data']
            page += 1
            if not result["has_more"] or page >= max_pages:
                break
        return results


class App:
    type = None

    def __init__(self, client: 'DifyBaseClient', id: str):
        self.client = client
        self.id = id

    @classmethod
    def create(cls, client: 'DifyBaseClient', id: str, mode: AppType) -> 'App':
        if mode == AppType.workflow:
            return WorkflowApp(client=client, id=id)
        elif mode == AppType.agent:
            return AgentApp(client=client, id=id)
        elif mode == AppType.chat:
            return ChatApp(client=client, id=id)
        elif mode == AppType.completion:
            return CompletionApp(client=client, id=id)
        elif mode == AppType.advanced_chat:
            return AdvancedChatApp(client=client, id=id)
        else:
            warnings.warn(f"Invalid mode: {mode}")
            return cls(client=client, id=id)

    def delete(self):
        self.client.delete_app(app_id=self.id)

    def export_yaml(self):
        url = f"{self.client.base_url}/console/api/apps/{self.id}/export?include_secret=false"
        return self.client._send_user_request("GET", url)["data"]

    @property
    def info(self) -> dict:
        url = f"{self.client.base_url}/console/api/apps/{self.id}"
        return self.client._send_user_request("GET", url)

    def update_info(self, info: dict):
        url = f"{self.client.base_url}/console/api/apps/{self.id}"
        self.client._send_user_request("PUT", url, json=info)

    @property
    def tokens(self) -> list[AppToken]:
        url = f"{self.client.base_url}/console/api/apps/{self.id}/api-keys"
        response = self.client._send_user_request("GET", url)
        return [AppToken(**token) for token in response["data"]]

    def create_token(self) -> AppToken:
        url = f"{self.client.base_url}/console/api/apps/{self.id}/api-keys"
        response = self.client._send_user_request("POST", url)
        return AppToken(**response)

    @property
    def token(self) -> AppToken:
        tokens = self.tokens
        if len(tokens) == 0:
            return self.create_token()
        return tokens[0]

    @property
    def chats(self) -> list[Chat]:
        def get_chats(page=1):
            url = f"{self.client.base_url}/console/api/apps/{self.id}/chat-conversations?page={page}&limit=100"
            response = self.client._send_user_request("GET", url)
            chats = [
                Chat(client=self.client, app=self,
                     id=chat_info['id'], info=chat_info)
                for chat_info in response['data']
            ]
            return chats, response['has_more']

        results = []
        page = 1
        while True:
            chats, has_more = get_chats(page)
            results += chats
            page += 1
            if not has_more:
                return results


class WorkflowApp(App):
    type = AppType.workflow

    def update_draft(self, draft: WorkflowDraft):
        url = f"{self.client.base_url}/console/api/apps/{self.id}/workflows/draft"
        self.client._send_user_request("POST", url, json=draft.model_dump())

    def get_draft(self) -> WorkflowDraft:
        url = f"{self.client.base_url}/console/api/apps/{self.id}/workflows/draft"
        return WorkflowDraft(**self.client._send_user_request("GET", url))

    def import_yaml(self, yaml_content) -> str:
        url = f"{self.client.base_url}/console/api/apps/imports"
        body = {
            "mode": "yaml-content",
            "yaml_content": yaml_content,
            "app_id": self.id,
        }
        result = self.client._send_user_request("POST", url, json=body)
        self.id = result.get("app_id")

    def publish(self):
        url = f"{self.client.base_url}/console/api/apps/{self.id}/workflows/publish"
        self.client._send_user_request("POST", url)

    def publish_as_tool(self, config: WorkflowToolProviderInfo):
        """
        returns workflow tool id
        """
        if config.workflow_tool_id is None:
            url = f"{self.client.base_url}/console/api/workspaces/current/tool-provider/workflow/create"
        else:
            url = f"{self.client.base_url}/console/api/workspaces/current/tool-provider/workflow/update"
        self.client._send_user_request("POST", url, json=config.model_dump())

    @property
    def tool_info(self) -> WorkflowToolProviderInfo:
        url = f"{self.client.base_url}/console/api/workspaces/current/tool-provider/workflow/get"
        params = {"workflow_app_id": self.id}
        response = self.client._send_user_request("GET", url, params=params)
        return WorkflowToolProviderInfo(**response)

    def get_logs(self, page: int = 1, limit: int = 10) -> PaginatedWorkflowLogs:
        url = f"{self.client.base_url}/console/api/apps/{self.id}/workflow-app-logs?page={page}&limit={limit}"
        response = self.client._send_user_request("GET", url)
        return PaginatedWorkflowLogs(**response)

    def iter_logs(self, limit: int = 10) -> Generator[WorkflowLogEntry, None, None]:
        page = 1
        while True:
            response = self.get_logs(page=page, limit=limit)
            yield from response.data
            if not response.has_more:
                break
            page += 1

    def get_node_executions(self, workflow_run_id: str) -> WorkflowNodeExecutions:
        """Get node executions for a specific workflow run."""
        url = f"{self.client.base_url}/console/api/apps/{self.id}/workflow-runs/{workflow_run_id}/node-executions"
        response = self.client._send_user_request("GET", url)
        return WorkflowNodeExecutions(**response)


class AgentApp(App):
    type = AppType.agent

    def import_yaml(self, yaml_content) -> str:
        yaml_dict = yaml.safe_load(yaml_content)
        url = f"{self.client.base_url}/console/api/apps/{self.id}/model-config"
        self.client._send_user_request("POST", url, json=yaml_dict["model_config"])
        self.update_info(yaml_dict["app"])
        return self.id

    def get_logs(self, page: int = 1, limit: int = 10) -> PaginatedAgentLogs:
        url = f"{self.client.base_url}/console/api/apps/{self.id}/chat-conversations?page={page}&limit={limit}"
        response = self.client._send_user_request("GET", url)
        return PaginatedAgentLogs(**response)

    def iter_logs(self, limit: int = 10) -> Generator[AgentConversation, None, None]:
        page = 1
        while True:
            response = self.get_logs(page=page, limit=limit)
            yield from response.data
            if not response.has_more:
                break
            page += 1

    def get_messages(self, conversation_id: str, limit: int = 10, page: int = 1) -> PaginatedChatMessages:
        """
        Get chat messages for a specific conversation.
        
        Args:
            conversation_id: The ID of the conversation to get messages from
            limit: Maximum number of messages to return (default: 10)
            page: Page number to retrieve (default: 1)
            
        Returns:
            PaginatedChatMessages containing 'data' (list of ChatMessage objects) and 'has_more' (bool) fields
        """
        url = f"{self.client.base_url}/console/api/apps/{self.id}/chat-messages?conversation_id={conversation_id}&limit={limit}&page={page}"
        response = self.client._send_user_request("GET", url)
        # Ensure required fields are present for PaginatedResponse
        if 'page' not in response:
            response['page'] = page
        if 'limit' not in response:
            response['limit'] = limit
        if 'total' not in response:
            response['total'] = len(response.get('data', []))
        return PaginatedChatMessages(**response)


class ChatApp(App):
    type = AppType.chat

    def get_logs(self, page: int = 1, limit: int = 10) -> PaginatedAgentLogs:
        url = f"{self.client.base_url}/console/api/apps/{self.id}/chat-conversations?page={page}&limit={limit}"
        response = self.client._send_user_request("GET", url)
        return PaginatedAgentLogs(**response)

    def iter_logs(self, limit: int = 10) -> Generator[AgentConversation, None, None]:
        page = 1
        while True:
            response = self.get_logs(page=page, limit=limit)
            yield from response.data
            if not response.has_more:
                break
            page += 1


class CompletionApp(App):
    type = AppType.completion


class AdvancedChatApp(ChatApp, WorkflowApp):
    type = AppType.advanced_chat
