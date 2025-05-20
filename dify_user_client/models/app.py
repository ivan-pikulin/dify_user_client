from typing import Optional, List, Dict, Literal
from enum import Enum

from .base import BaseModel

class AppType(str, Enum):
    WORKFLOW = "workflow"
    CHAT = "chat"
    ADVANCED_CHAT = "advanced-chat"
    AGENT_CHAT = "agent-chat"
    COMPLETION = "completion"

class AppToken(BaseModel):
    type: Literal["app"]
    token: str
    last_used_at: Optional[int] = None

class GraphNodeDataTypes(str, Enum):
    START = "start"
    END = "end"
    LLM = "llm"

class GraphNodeData(BaseModel):
    type: GraphNodeDataTypes
    title: str
    description: str
    variables: List

class GraphEdgeData(BaseModel):
    sourceType: GraphNodeDataTypes
    targetType: GraphNodeDataTypes
    isInIteration: bool

class GraphNode(BaseModel):
    type: str
    data: Dict
    position: Dict
    targetPosition: str
    sourcePosition: str
    positionAbsolute: Dict
    width: int
    height: int

class GraphEdge(BaseModel):
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
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    viewport: Viewport = Viewport()

class WorkflowDraft(BaseModel):
    graph: Optional[Graph] = Graph()
    features: Dict = {}
    environment_variables: List = []
    conversation_variables: List = [] 