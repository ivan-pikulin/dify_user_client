from typing import TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    limit: int
    total: int
    has_more: bool
    data: List[T]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data) 