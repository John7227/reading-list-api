from typing import Optional, List
from uuid import UUID
from models.book import BookCreate, Book, BookUpdate
from repositories.book_repository import BookRepository

class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def create_book(self, book_data: BookCreate) -> Book:
        book = Book(**book_data.model_dump())
        return self.repository.add(book)

    def get_book(self, book_id: UUID) -> Optional[Book]:
        return self.repository.get(book_id)

    def get_books(self) -> List[Book]:
        return self.repository.list()

    def update_book(self, book_id: UUID, book_data: BookUpdate) -> Optional[Book]:
        update_data = book_data.model_dump(exclude_unset=True)
        return self.repository.update(book_id, update_data)

    def delete_book(self, book_id: UUID) -> bool:
        return self.repository.delete(book_id)