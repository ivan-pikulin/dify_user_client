from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field

from .pagination import PaginatedResponse


class WorkflowRun(BaseModel):
    id: str
    version: str
    status: str
    error: Optional[str]
    elapsed_time: float
    total_tokens: int
    total_steps: int
    created_at: int
    finished_at: int
    exceptions_count: int


class WorkflowLogEntry(BaseModel):
    id: str
    workflow_run: WorkflowRun
    created_from: str
    created_by_role: str
    created_by_account: Optional[Dict]
    created_by_end_user: Dict
    created_at: int


class AgentConversation(BaseModel):
    id: str
    status: str
    from_source: str
    from_end_user_id: Optional[str]
    from_end_user_session_id: Optional[str]
    from_account_id: Optional[str]
    from_account_name: Optional[str]
    name: str
    summary: str
    read_at: Optional[int]
    created_at: int
    updated_at: int
    annotated: bool
    agent_model_config: Dict = Field(alias="model_config")
    message_count: int
    user_feedback_stats: Dict
    admin_feedback_stats: Dict
    status_count: Dict


class PaginatedWorkflowLogs(PaginatedResponse[WorkflowLogEntry]):
    pass


class PaginatedAgentLogs(PaginatedResponse[AgentConversation]):
    pass


class WorkflowNodeExecutionMetadata(BaseModel):
    parallel_id: Optional[str] = None
    parallel_start_node_id: Optional[str] = None
    tool_info: Optional[Dict[str, Any]] = None
    total_tokens: Optional[int] = None
    total_price: Optional[str] = None
    currency: Optional[str] = None


class WorkflowNodeExecution(BaseModel):
    id: str
    index: int
    predecessor_node_id: Optional[str]
    node_id: str
    node_type: str
    title: str
    inputs: Optional[Dict[str, Any]]
    process_data: Optional[Dict[str, Any]]
    outputs: Optional[Dict[str, Any]]
    status: str
    error: Optional[str]
    elapsed_time: float
    execution_metadata: Optional[WorkflowNodeExecutionMetadata]
    extras: Dict[str, Any]
    created_at: int
    created_by_role: str
    created_by_account: Optional[Dict[str, Any]]
    created_by_end_user: Dict[str, Any]
    finished_at: int


class WorkflowNodeExecutions(BaseModel):
    data: List[WorkflowNodeExecution]


class ChatMessage(BaseModel):
    """Represents a single chat message in a conversation."""
    id: str
    conversation_id: str
    inputs: Optional[Dict[str, Any]] = None
    query: Optional[str] = None
    answer: Optional[str] = None
    message: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    created_at: int
    created_by_role: Optional[str] = None
    created_by_account: Optional[Dict[str, Any]] = None
    created_by_end_user: Optional[Dict[str, Any]] = None
    from_source: Optional[str] = None
    from_end_user_id: Optional[str] = None
    from_end_user_session_id: Optional[str] = None
    from_account_id: Optional[str] = None
    from_account_name: Optional[str] = None
    
    class Config:
        extra = 'allow'  # Allow additional fields from API


class PaginatedChatMessages(PaginatedResponse[ChatMessage]):
    """Paginated response for chat messages."""
    pass 