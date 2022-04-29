from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status

from fastapi.security import OAuth2PasswordRequestForm

from prod.app.documents.document import Book, User
from prod.app.auth.auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from prod.config import settings
from prod.app.models.models import Token

router = APIRouter(prefix="")


@router.post("/signup")
async def signup(user_data: User):
    user_data.password = get_password_hash(user_data.password)
    await user_data.save()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/add/book", status_code=201)
async def add_book(book: Book, current_user: User = Depends(get_current_user)):
    return await book.save()


@router.get("/api/get/all/book", status_code=200)
async def get_all_book_from_library():
    return await Book.find_all().to_list()


@router.get("/api/get/book/{genre}", status_code=200)
async def get_all_genre_from_library(genre):
    return await Book.find_many(Book.genrre == genre).to_list()


@router.get("/api/get/author/{author}", status_code=200)
async def get_all_author_from_library(author):
    return await Book.find_many(Book.author == author).to_list()


