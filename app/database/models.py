from sqlalchemy import Column, String, DateTime, Integer, Table, ForeignKey, MetaData, LargeBinary, func, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base, engine
from uuid import uuid4
from datetime import datetime


metadata = MetaData()


book_authors = Table(
    'book_authors',
    Base.metadata,
    Column('book_id', UUID, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    Column('author_id', UUID, ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True)
)

book_genres = Table(
    'book_genres',
    Base.metadata,
    Column('book_id', UUID, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', UUID, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)

reader_books = Table(
    'reader_books',
    Base.metadata,
    Column('reader_id', UUID, ForeignKey('readers.id', ondelete='CASCADE'), primary_key=True),
    Column('book_id', UUID, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    Column('output_date', DateTime, default=datetime.utcnow),
    Column('input_date', DateTime, nullable=True)
)


class Book(Base):
    __tablename__ = 'books'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    published_at = Column(DateTime, default=datetime.utcnow)
    count_available = Column(Integer, default=0)

    authors = relationship('Author', secondary=book_authors, back_populates='books')
    genres = relationship('Genre', secondary=book_genres, back_populates='books')


class Author(Base):
    __tablename__ = 'authors'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    password = Column(LargeBinary)
    biography = Column(String)
    birthday = Column(DateTime)

    books = relationship('Book', secondary=book_authors, back_populates='authors')


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)

    books = relationship('Book', secondary=book_genres, back_populates='genres')


class UserReader(Base):
    __tablename__ = 'readers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String)
    password = Column(LargeBinary)
    info = Column(String)
    can_get_more = Column(Integer, default=5)
    email = Column(String)

    books = relationship('Book', secondary=reader_books, backref='readers')


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String)
    password = Column(LargeBinary)


class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    at_time = Column(DateTime, server_default=func.now())
    level = Column(String)
    message = Column(String)
    context = Column(JSON)


Base.metadata.create_all(bind=engine)

