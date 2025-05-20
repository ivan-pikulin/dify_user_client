from typing import Optional, TypeVar, Generic
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, Field

T = TypeVar('T')

class BaseModel(PydanticBaseModel):
    """Base model with common functionality"""
    id: Optional[str] = Field(None, description="Unique identifier")
    created_at: Optional[int] = Field(None, description="Creation timestamp")
    updated_at: Optional[int] = Field(None, description="Last update timestamp")

    def to_dict(self):
        return self.model_dump()

    @property
    def created_datetime(self) -> Optional[datetime]:
        if self.created_at:
            return datetime.fromtimestamp(self.created_at)
        return None

    @property
    def updated_datetime(self) -> Optional[datetime]:
        if self.updated_at:
            return datetime.fromtimestamp(self.updated_at)
        return None

class BaseResponse(PydanticBaseModel, Generic[T]):
    """Base response model for API responses"""
    data: T
    has_more: Optional[bool] = False
    total: Optional[int] = None
    error: Optional[str] = None 