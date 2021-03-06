from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status

from fastapi.security import OAuth2PasswordRequestForm

from prod.app.documents.document import Book, User
from prod.app.auth.auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from prod.config import settings
from prod.app.models.models import Token

router = APIRouter(prefix="")


async def get_materials(option, target):
    if books := await Book.find_many(option == target).to_list():
        return books
    raise HTTPException(status_code=400, detail="not found")


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
    if books := await Book.find_many(Book.genre == genre).to_list():
        return books
    raise HTTPException(status_code=400, detail="not found")


@router.get("/api/get/author/{author}", status_code=200)
async def get_all_author_from_library(author):
    if books := await Book.find_many(Book.author == author).to_list():
        return books
    raise HTTPException(status_code=400, detail="not found")


@router.put("/api/update/book{name}")
async def update_book(name: str, new_name: str, current_user: User = Depends(get_current_user)):
    if book := await Book.find_one(Book.name == name):
        book.name = new_name
        return await book.save()
    raise HTTPException(status_code=400, detail="not found")


@router.delete("/api/delete/book/{name}")
async def delete_book_bame(name, current_user: User = Depends(get_current_user)):
    if book := Book.find_one(Book.name == name):
        await book.delete()
        return {"book": "deleted"}
    raise HTTPException(status_code=400, detail="not found")