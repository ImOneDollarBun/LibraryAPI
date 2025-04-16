from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Literal
from uuid import UUID


class UserSchema(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    role: Literal['reader', 'admin']


class User(BaseModel):
    username: str
    password: str
    role: Literal['reader', 'admin']


class Genres(BaseModel):
    names: List[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class BookCreate(BaseModel):
    name: str
    description: str
    published_at: Optional[datetime] = None
    genres: List[str]
    count_available: int
    authors: List[str]


class AuthorOut(BaseModel):
    id: UUID
    username: str

    class Config:
        from_attributes = True


class GenreOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class BookOut(BaseModel):
    id: UUID
    name: str
    description: str
    published_at: Optional[datetime]
    count_available: int
    authors: List[AuthorOut]
    genres: List[GenreOut]

    class Config:
        from_attributes = True


class AuthorCreate(BaseModel):
    username: str
    biography: Optional[str] = None
    birthday: Optional[datetime] = None


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: Optional[EmailStr] = None
    role: Literal['admin', 'reader', 'author']

    class Config:
        from_attributes = True
