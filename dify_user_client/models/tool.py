from typing import Optional, Union, Dict, Any, Literal, List
from pydantic import Field

from .base import BaseModel

class ToolParameterOption(BaseModel):
    value: str
    label: Union[Dict, str]

class ToolParameter(BaseModel):
    name: str
    label: Union[Dict, str]
    human_description: Optional[Union[Dict, str]] = None
    placeholder: Optional[Union[Dict, str]] = None
    type: Literal["string", "number", "boolean", "select", "file", "files", "secret-input"]
    form: Literal["llm", "form"]
    llm_description: Optional[str] = None
    required: bool
    default: Optional[Any] = None
    min: Optional[float] = None
    max: Optional[float] = None
    options: Optional[List[ToolParameterOption]] = None

class ToolInfo(BaseModel):
    author: str
    name: str
    label: Union[Dict, str]
    description: Union[Dict, str]
    parameters: List[ToolParameter]
    labels: List[str]

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
    parameters: List[WorkflowToolParameter]
    tool: ToolInfo 