from typing import Optional, Dict, Any, List
from enum import Enum

from .base import BaseModel
from .pagination import PaginatedResponse

class WorkflowStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowRun(BaseModel):
    version: str
    status: WorkflowStatus
    error: Optional[str] = None
    elapsed_time: float
    total_tokens: int
    total_steps: int
    finished_at: int
    exceptions_count: int

class WorkflowLogEntry(BaseModel):
    workflow_run: WorkflowRun
    created_from: str
    created_by_role: str
    created_by_account: Optional[Dict]
    created_by_end_user: Dict

class WorkflowNodeExecutionMetadata(BaseModel):
    parallel_id: Optional[str] = None
    parallel_start_node_id: Optional[str] = None
    tool_info: Optional[Dict[str, Any]] = None
    total_tokens: Optional[int] = None
    total_price: Optional[str] = None
    currency: Optional[str] = None

class WorkflowNodeExecution(BaseModel):
    index: int
    predecessor_node_id: Optional[str]
    node_id: str
    node_type: str
    title: str
    inputs: Optional[Dict[str, Any]]
    process_data: Optional[Dict[str, Any]]
    outputs: Optional[Dict[str, Any]]
    status: WorkflowStatus
    error: Optional[str]
    elapsed_time: float
    execution_metadata: Optional[WorkflowNodeExecutionMetadata]
    extras: Dict[str, Any]
    created_by_role: str
    created_by_account: Optional[Dict[str, Any]]
    created_by_end_user: Dict[str, Any]
    finished_at: int

class WorkflowNodeExecutions(BaseModel):
    data: List[WorkflowNodeExecution]

class PaginatedWorkflowLogs(PaginatedResponse[WorkflowLogEntry]):
    """Paginated response for workflow logs"""
    pass 