import json

import pytest
from main import app
from uuid import uuid4
from fastapi.testclient import TestClient
from dependencies import get_book_repository
from repositories.in_memory_book_repository import InMemoryBookRepository

@pytest.fixture
def client():
    repository = InMemoryBookRepository()

    app.dependency_overrides[get_book_repository] = lambda: repository

    yield TestClient(app)
    app.dependency_overrides.clear()

def test_create_book_returns_201_and_created_book(client):
    response = client.post(
        "/books",
        json={
            "title": "Atomic Habits",
            "author": "James Clear",
            "status": "to_read"
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Atomic Habits"
    assert response.json()["author"] == "James Clear"

def test_get_books_returns_all_books(client):
    client.post(
        "/books",
        json={
            "title": "Atomic Habits",
            "author": "James Clear",
        }
    )

    client.post(
        "/books",
        json={
            "title": "The psychology of money",
            "author": "Housel Morgan",
        }
    )

    response = client.get("/books")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_missing_book_returns_404(client):
    response = client.get(f"/books/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_update_missing_returns_404(client):
    response = client.patch(f"/books/{uuid4()}", json = {"title": "The psychology of money"})

    assert response.status_code == 404

def test_delete_missing_book_returns_404(client):
    response = client.delete(f"/books/{uuid4()}")

    assert response.status_code == 404

def test_create_book_with_invalid_data_returns_422(client):
    response = client.post(
        "/books",
        json={
            "title": "",
            "author": "James Clear",
        }
    )

    assert response.status_code == 422

def test_full_crud_flow(client):
    create_response = client.post(
        "/books",
        json={
            "title": "Atomic Habits",
            "author": "James Clear",
            "status": "to_read",
        }
    )
    assert create_response.status_code == 201
    assert create_response.json()["title"] == "Atomic Habits"


    book_id = create_response.json()["id"]
    get_response = client.get(f"/books/{book_id}")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Atomic Habits"



    update_response = client.patch(
        f"/books/{book_id}",
        json={
            "title": "The psychology of money",
            "status": "reading"
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "The psychology of money"
    assert update_response.json()["author"] == "James Clear"
    assert update_response.json()["status"] == "reading"



    delete_response = client.delete(f"/books/{book_id}")

    assert delete_response.status_code == 204

    get_deleted_response = client.get(f"/books/{book_id}")
    assert get_deleted_response.status_code == 404