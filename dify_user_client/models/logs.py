from typing import Optional, Dict
from pydantic import BaseModel

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
    model_config: Dict
    message_count: int
    user_feedback_stats: Dict
    admin_feedback_stats: Dict
    status_count: Dict


class PaginatedWorkflowLogs(PaginatedResponse[WorkflowLogEntry]):
    pass


class PaginatedAgentLogs(PaginatedResponse[AgentConversation]):
    pass 