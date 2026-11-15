from fastapi import Depends

from repositories.in_memory_book_repository import InMemoryBookRepository
from repositories.book_repository import BookRepository
from services.book_service import BookService

book_repository = InMemoryBookRepository()

def get_book_repository() -> BookRepository:
    return book_repository

def get_book_service( repository: BookRepository = Depends(get_book_repository)) -> BookService:
    return BookService(repository)