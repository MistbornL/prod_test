from typing import Optional, List

from beanie import Document


class User(Document):
    email: str
    password: str
