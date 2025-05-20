from typing import TypeVar, Generic, List
from pydantic import Field

from .base import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of items per page")
    total: int = Field(..., description="Total number of items")
    has_more: bool = Field(..., description="Whether there are more pages")
    data: List[T] = Field(..., description="List of items in the current page")

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data) 