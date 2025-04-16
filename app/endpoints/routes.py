from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Cookie, Response, Body
from app.schemas import UserSchema, Token, BookCreate, BookOut, AuthorCreate, AuthorOut, User, Genres
from app.utils.jwt_secure import encode_jwt, check_password, decode_jwt
from app.crud import (
    create_user, get_user_by_username, create_book,
    get_books, get_book_by_id, create_author, get_authors, create_genre, readers, give_book
)


router = APIRouter()


@router.post('/register', response_model=Token)
async def registration(response: Response, data: UserSchema):
    db_user = get_user_by_username(data.username, data.role)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(data)

    jwt_payload = {
        'username': data.username,
        'role': data.role
    }

    token = encode_jwt(jwt_payload)

    response.set_cookie('access_token', token, max_age=1200)
    return Token(access_token=token, token_type='Bearer')


@router.post('/login', response_model=Token)
async def auth(response: Response, form_data: User):
    db_user = get_user_by_username(form_data.username, form_data.role)
    if not db_user or not check_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    jwt_payload = {
        'username': db_user.username,
        'role': form_data.role
    }

    token = encode_jwt(jwt_payload)

    response.set_cookie('access_token', token, max_age=600)
    return Token(access_token=token, token_type='Bearer')


@router.get('/readers')
async def get_readers(access_token: str = Cookie()):
    role = decode_jwt(access_token)['role']
    if role == 'admin':
        return readers()
    return HTTPException(status_code=401)


@router.post('/give_book')
async def give_book_view(
    user: UUID | str,
    book_id: UUID = Body(...),
    access_token: str = Cookie()
):
    role = decode_jwt(access_token)['role']
    if role != 'admin':
        raise HTTPException(status_code=403, detail="Only admins can give books")

    try:
        give_book(user, book_id)
        return {"detail": "Книга успешно выдана"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/genres')
async def create_genres(genres: Genres, access_token: str = Cookie()):
    role = decode_jwt(access_token)['role']
    if role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return create_genre(genres)


@router.post('/books', response_model=BookOut)
async def create_book_view(book: BookCreate, access_token: str = Cookie()):
    role = decode_jwt(access_token)['role']
    if role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return create_book(book)


@router.get('/books', response_model=list[BookOut])
async def list_books():
    return get_books()


@router.get('/books/{book_id}', response_model=BookOut)
async def get_book(book_id: UUID):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post('/authors')
async def create_author_view(author: AuthorCreate, access_token: str = Cookie()):
    role = decode_jwt(access_token)['role']
    if role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return create_author(author)


@router.get('/authors', response_model=list[AuthorOut])
async def list_authors():
    return get_authors()