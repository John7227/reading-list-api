from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class BookStatus(str, Enum):
    TO_READ = "to_read"
    READING = "reading"
    COMPLETED = "completed"

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    status: BookStatus = BookStatus.TO_READ

class Book(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    author: str
    status: BookStatus = BookStatus.TO_READ

class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    author: Optional[str] = Field(default=None, min_length=1)
    status: Optional[BookStatus] = None