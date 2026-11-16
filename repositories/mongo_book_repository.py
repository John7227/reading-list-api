from typing import Optional, List
from uuid import UUID

from database import books_collection
from models.book import Book
from repositories.book_repository import BookRepository


class MongoBookRepository(BookRepository):

    def add(self, book: Book) -> Book:
        book_data = book.model_dump(mode="json")
        book_data["_id"] = str(book.id)
        del book_data["id"]
        books_collection.insert_one(book_data)

        return book

    def get(self, book_id: UUID) -> Optional[Book]:
        book_data = books_collection.find_one({"_id": str(book_id)})
        if book_data is None:
            return None

        book_data["id"] = book_data.pop("_id")

        return Book(**book_data)

    def list(self) -> List[Book]:
        books = []
        for book_data in books_collection.find():
            book_data["id"] = book_data.pop("_id")
            books.append(Book(**book_data))

        return books

    def update(self, book_id: UUID, data: dict) -> Optional[Book]:
        books_collection.update_one({"_id": str(book_id)}, {"$set": data})

        return self.get(book_id)

    def delete(self, book_id: UUID) -> bool:
        result = books_collection.delete_one({"_id": str(book_id)})

        return result.deleted_count > 0