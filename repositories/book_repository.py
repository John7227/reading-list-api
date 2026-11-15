from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from models.book import Book


class BookRepository(ABC):

    @abstractmethod
    def add(self, book: Book) -> Book:
        pass

    @abstractmethod
    def get(self, book_id: UUID) -> Optional[Book]:
        pass

    @abstractmethod
    def list(self) -> List[Book]:
        pass

    @abstractmethod
    def update(self, book_id: UUID, data: dict) -> Optional[Book]:
        pass

    @abstractmethod
    def delete(self, book_id: UUID) -> bool:
        pass