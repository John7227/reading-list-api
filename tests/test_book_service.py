from uuid import uuid4
import pytest
from models.book import BookCreate, BookStatus, BookUpdate
from repositories.in_memory_book_repository import InMemoryBookRepository
from services.book_service import BookService

def test_create_book():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    book_data = BookCreate(
        title="Atomic Habits",
        author="James Clear",
        status=BookStatus.TO_READ,
    )

    book = service.create_book(book_data)

    assert book.title == "Atomic Habits"
    assert book.author == "James Clear"
    assert book.status == BookStatus.TO_READ

def test_create_book_with_empty_title_raises_exception():
    with pytest.raises(Exception):
        BookCreate(
            title="",
            author="James Clear",
        )

def test_create_book_with_empty_author_raises_exception():
    with pytest.raises(Exception):
        BookCreate(
            title="The psychology of money",
            author="",
        )

def test_create_book_with_invalid_status_raises_exception():
    with pytest.raises(Exception):
        BookCreate(
            title="Atomic Habits",
            author="James Clear",
            status="Invalid_status",
        )

def test_get_book_returns_the_book():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    book_data = BookCreate(
        title="Atomic Habits",
        author="James Clear",
        status=BookStatus.READING,
    )

    created_book = service.create_book(book_data)
    book = service.get_book(created_book.id)

    assert book.id == created_book.id
    assert book.title == "Atomic Habits"
    assert book.author == "James Clear"
    assert book.status == BookStatus.READING

def test_get_book_not_found_is_none():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    book = service.get_book(uuid4())

    assert book is None

def test_get_books():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    book_one = BookCreate(
        title="Atomic Habits",
        author="James Clear",
        status=BookStatus.TO_READ,
    )

    book_two = BookCreate(
        title="The psychology of money",
        author="Housel Morgan",
        status=BookStatus.READING,
    )

    first_created_book = service.create_book(book_one)
    second_created_book = service.create_book(book_two)

    books = service.get_books()

    assert len(books) == 2
    assert first_created_book.title == "Atomic Habits"
    assert second_created_book.title == "The psychology of money"

def test_get_books_when_there_is_no_book_returns_an_empty_list():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    books = service.get_books()

    assert len(books) == 0
    assert books == []

def test_update_book():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    created_book = service.create_book(
        BookCreate(
            title="Atomic Habits",
            author="James Clear",
            status=BookStatus.TO_READ,
        )
    )

    update_data = BookUpdate(
        title="The psychology of money",
        status=BookStatus.READING
    )

    updated_data = service.update_book(created_book.id, update_data)

    assert updated_data.title == "The psychology of money"
    assert updated_data.author == "James Clear"
    assert updated_data.status == BookStatus.READING

def test_update_book_with_empty_title_raises_exception():
    with pytest.raises(Exception):
        BookUpdate(title="")

def test_update_book_not_found_when_the_book_does_not_exist():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    update_book = BookUpdate(title="The psychology of money", status=BookStatus.TO_READ)

    updated_book = service.update_book(uuid4(), update_book)

    assert updated_book is None

def test_delete_book_deletes_the_book():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    created_book = service.create_book(
        BookCreate(
            title="Atomic Habits",
            author="James Clear",
            status=BookStatus.TO_READ,
        )
    )

    deleted = service.delete_book(created_book.id)

    assert deleted is True
    assert service.get_book(created_book.id) is None

def test_delete_book_not_found_returns_false():
    repository = InMemoryBookRepository()
    service = BookService(repository)

    deleted = service.delete_book(uuid4())

    assert deleted is False