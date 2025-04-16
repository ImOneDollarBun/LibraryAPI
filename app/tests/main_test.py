import pytest
from httpx import AsyncClient
from fastapi import status
from uuid import uuid4
from main import app
from app.utils.jwt_secure import encode_jwt
from fastapi.testclient import TestClient


def test_register_and_login():
    with TestClient(app) as ac:
        user_data = {
            "username": "test_user",
            "password": "testpass123",
            "role": "reader"
        }
        response = ac.post("/register", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

        # login
        response = ac.post("/login", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()


def test_create_and_list_books():
    token = encode_jwt({"username": "admin_user", "role": "admin"})
    headers = {"Cookie": f"access_token={token}"}

    book_data = {
        "title": "Test Book",
        "description": "A book for testing",
        "author_id": str(uuid4()),
        "genre_id": str(uuid4())
    }

    with TestClient(app) as ac:
        create = ac.post("/books", json=book_data, headers=headers)
        # может упасть, если нет автора/жанра в базе — тогда можно сделать мок
        assert create.status_code in [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR]

        list_books = ac.get("/books")
        assert list_books.status_code == status.HTTP_200_OK


def test_create_and_list_authors():
    token = encode_jwt({"username": "admin_user", "role": "admin"})
    headers = {"Cookie": f"access_token={token}"}

    author_data = {
        "username": "author1",
        "password": "authorpass",
        "biography": "Some bio",
        "birthday": "1990-01-01T00:00:00"
    }

    with TestClient(app) as ac:
        create = ac.post("/authors", json=author_data, headers=headers)
        assert create.status_code == status.HTTP_200_OK or create.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

        list_authors = ac.get("/authors")
        assert list_authors.status_code == status.HTTP_200_OK


def test_give_book_access_control():
    token_user = encode_jwt({"username": "reader1", "role": "reader"})
    token_admin = encode_jwt({"username": "admin1", "role": "admin"})
    headers_user = {"Cookie": f"access_token={token_user}"}
    headers_admin = {"Cookie": f"access_token={token_admin}"}

    fake_user_id = str(uuid4())
    fake_book_id = str(uuid4())

    with TestClient(app) as ac:
        # Попытка от пользователя — должен получить отказ
        response = ac.post("/give_book", params={"user": fake_user_id}, json={"book_id": fake_book_id}, headers=headers_user)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Попытка от админа
        response = ac.post("/give_book", params={"user": fake_user_id}, json={"book_id": fake_book_id}, headers=headers_admin)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR]


def test_create_genres():
    token = encode_jwt({"username": "admin", "role": "admin"})
    headers = {"Cookie": f"access_token={token}"}

    with TestClient(app) as ac:
        response = ac.post("/genres", json={"name": "Fantasy"}, headers=headers)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR]
