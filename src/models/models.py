import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    name: str
    surname: str
    login: str
    password: str
    birthdate: datetime.date
    blocked: bool = True
    admin: bool = False
    readonly: bool = True


class UserSafe(BaseModel):
    name: str
    surname: str
    login: str
    birthdate: datetime.date
    blocked: bool = True
    admin: bool = False
    readonly: bool = True


class UserOne(BaseModel):
    item: UserSafe


class UserMany(BaseModel):
    items: List[UserSafe]


class UserAuth(BaseModel):
    login: str
    password: str
