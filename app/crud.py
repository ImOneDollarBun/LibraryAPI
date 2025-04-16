from datetime import datetime
from typing import Literal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import SessionLocal
from app.schemas import UserSchema, BookCreate, AuthorCreate, UserResponse, Genres
from app.database.models import UserReader, Admin, Book, Author, Genre, reader_books
from app.utils.jwt_secure import hash_password


def create_user(user: UserSchema):
    session = SessionLocal()
    try:
        hashed_pwd = hash_password(user.password)
        if user.role == 'admin':
            new_user = Admin(
                username=user.username,
                password=hashed_pwd
            )
        elif user.role == 'reader':
            new_user = UserReader(
                username=user.username,
                email=user.email,
                password=hashed_pwd
            )

        else:
            new_user = Author(
                username=user.username,
                password=hashed_pwd
            )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=getattr(new_user, 'email', None),
            role=user.role
        )
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_user_by_username(username: str, role: str):
    session = SessionLocal()
    try:
        if role == 'reader':
            user = session.query(UserReader).filter(UserReader.username == username).first()
        elif role == 'author':
            user = session.query(Author).filter(Author.username == username).first()
        else:
            user = session.query(Admin).filter(Admin.username == username).first()

        return user
    finally:
        session.close()


def create_genre(genres: Genres):
    session = SessionLocal()

    try:
        for genre in genres.names:
            new_genre = Genre(
                name=genre
            )

            session.add(new_genre)
            session.commit()
            session.refresh(new_genre)

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_book(book: BookCreate):
    session = SessionLocal()
    try:
        authors = [get_something_id(Author, x) for x in book.authors]
        genres = [get_something_id(Genre, x) for x in book.genres]

        new_book = Book(
            name=book.name,
            description=book.description,
            published_at=book.published_at,
            count_available=book.count_available,
            authors=authors,
            genres=genres
        )
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        new_book = session.query(Book).options(
            joinedload(Book.authors),
            joinedload(Book.genres)
        ).filter_by(id=new_book.id).first()
        return new_book
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_books(skip=0, limit=10):
    session = SessionLocal()
    try:
        books = session.query(Book).options(
            joinedload(Book.authors),
            joinedload(Book.genres)
        ).all()
        return books
    finally:
        session.close()


def get_something_id(table, name):
    session = SessionLocal()
    try:
        if table == Genre:
            return session.query(table).filter(table.name == name).first()
        else:
            return session.query(table).filter(table.username == name).first()
    finally:
        session.close()


def get_book_by_id(book_id: UUID):
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == book_id).options(
            joinedload(Book.authors),
            joinedload(Book.genres)
        ).first()

        return book
    finally:
        session.close()


def update_book(book_id: UUID, book_data):
    session = SessionLocal()
    try:
        book = session.get(Book, book_id)
        if book:
            for key, value in book_data.dict(exclude_unset=True).items():
                if key in ['author_ids', 'genre_ids']:
                    if key == 'author_ids':
                        book.authors = session.query(Author).filter(Author.id.in_(value)).all()
                    elif key == 'genre_ids':
                        book.genres = session.query(Genre).filter(Genre.id.in_(value)).all()
                else:
                    setattr(book, key, value)
            session.commit()
            session.refresh(book)
        return book
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_book(book_id: UUID):
    session = SessionLocal()
    try:
        book = session.get(Book, book_id)
        if book:
            session.delete(book)
            session.commit()
        return book
    finally:
        session.close()


def create_author(author: AuthorCreate):
    session = SessionLocal()
    try:
        new_author = Author(
            username=author.username,
            biography=author.biography,
            birthday=author.birthday
        )
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
        return new_author
    finally:
        session.close()


def get_authors():
    session = SessionLocal()
    try:
        return session.query(Author).all()
    finally:
        session.close()


def readers():
    session = SessionLocal()
    try:
        return session.query(UserReader).all()
    finally:
        session.close()


def give_book(user: UUID | str, book_id: UUID):
    session = SessionLocal()

    try:
        if isinstance(user, str):
            user = get_something_id(UserReader, user).id  # предполагаем, что возвращает UUID

        # Проверяем, есть ли уже такая запись
        existing = session.execute(
            select(reader_books).where(
                (reader_books.c.reader_id == user) &
                (reader_books.c.book_id == book_id) &
                (reader_books.c.input_date is None)
            )
        ).first()

        if existing:
            raise ValueError("Книга уже выдана этому пользователю и не возвращена")

        session.execute(
            reader_books.insert().values(
                reader_id=user,
                book_id=book_id,
                output_date=datetime.utcnow()
            )
        )
        session.commit()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
