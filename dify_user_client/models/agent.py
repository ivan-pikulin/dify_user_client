from typing import Optional, Dict
from enum import Enum

from .base import BaseModel
from .pagination import PaginatedResponse

class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class AgentConversation(BaseModel):
    status: AgentStatus
    from_source: str
    from_end_user_id: Optional[str]
    from_end_user_session_id: Optional[str]
    from_account_id: Optional[str]
    from_account_name: Optional[str]
    name: str
    summary: str
    read_at: Optional[int]
    annotated: bool
    agent_model_config: Dict
    message_count: int
    user_feedback_stats: Dict
    admin_feedback_stats: Dict
    status_count: Dict

class PaginatedAgentLogs(PaginatedResponse[AgentConversation]):
    """Paginated response for agent logs"""
    pass 