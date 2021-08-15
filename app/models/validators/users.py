from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserSignup(UserLogin):
    @validator("password")
    def valid_password(cls, val):
        if len(val) < 8:
            raise ValueError("password cannot be less than 8 characters")
        if " " in val:
            raise ValueError("password cannot contain spaces")
        return val


class UsersDB(BaseModel):
    id: str
    password: Optional[str]
    name: Optional[str]
    email: str
    created_at: datetime
    updated_at: datetime


class UsersPaginate(BaseModel):
    results: List[UsersDB]


class AuthToken(BaseModel):
    token: str


class UserType(str, Enum):
    USER = "USER"
    AGENT = "AGENT"
    ADMIN = "ADMIN"

