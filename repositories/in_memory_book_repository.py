from typing import List, Optional
from uuid import UUID
from models.book import Book
from repositories.book_repository import BookRepository

class InMemoryBookRepository(BookRepository):

    def __init__(self):
        self._books: List[Book] = []

    def add(self, book: Book) -> Book:
        self._books.append(book)
        return book

    def get(self, book_id: UUID) -> Optional[Book]:
        for book in self._books:
            if book.id == book_id:
                return book

        return None

    def list(self) -> List[Book]:
        return self._books

    def update(self, book_id: UUID, data: dict) -> Optional[Book]:
        book = self.get(book_id)

        if book is None:
            return None

        updated_book = book.model_copy(update=data)

        index = self._books.index(book)
        self._books[index] = updated_book

        return updated_book

    def delete(self, book_id: UUID) -> bool:
        book = self.get(book_id)

        if book is None:
            return False

        self._books.remove(book)
        return True