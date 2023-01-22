import datetime
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


class UserAuth(BaseModel):
    login: str
    password: str
