from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from dependencies import get_book_service
from models.book import Book, BookCreate, BookUpdate
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate, service: BookService = Depends(get_book_service)):
    return service.create_book(book_data)

@router.get("/", response_model=List[Book])
def get_books(service: BookService = Depends(get_book_service)):
    return service.get_books()

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: UUID, service: BookService = Depends(get_book_service)):
    book = service.get_book(book_id)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.patch("/{book_id}", response_model=Book)
def update_book(book_id: UUID, book_data: BookUpdate, service: BookService = Depends(get_book_service)):
    book = service.update_book(book_id, book_data)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: UUID, service: BookService = Depends(get_book_service)):
    deleted = service.delete_book(book_id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return None