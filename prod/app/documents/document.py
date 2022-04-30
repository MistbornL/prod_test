from typing import Optional, List

from beanie import Document


class User(Document):
    email: str
    password: str


class Book(Document):
    genre: str
    author: str
    name: str
    date: Optional[int] = 0


class Library(Document):
    total: int = 0
