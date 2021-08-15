from enum import Enum

from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel


class ErrorTypes(str, Enum):
    USER_NOT_FOUND = "USER_NOT_FOUND"
    RUN_NOT_FOUND = "RUN_NOT_FOUND"
    EMAIL_EXISTS = "EMAIL_EXISTS"
    INCORRECT_PASSWORD = "INCORRECT_PASSWORD"
    REQUIRED_SCOPE_NOT_FOUND = "REQUIRED_SCOPE_NOT_FOUND"
    INVALID_TOKEN = "INVALID_TOKEN"
    USER_HAS_ONGOING_RUNS = "USER_HAS_ONGOING_RUNS"
    BAD_REQUEST = "BAD_REQUEST"
    RUN_NOT_IN_PROGRESS = "RUN_NOT_IN_PROGRESS"
    NOT_AN_ADMIN = "NOT_AN_ADMIN"


class ErrorResponse(BaseModel):
    msg: str
    type: ErrorTypes


def create_400_exception(
    code: ErrorTypes, message: str, headers: dict = {}
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorResponse(msg=message, type=code).dict(),
        headers=headers,
    )


def create_404_exception(
    code: ErrorTypes, message: str, headers: dict = {}
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrorResponse(msg=message, type=code).dict(),
        headers=headers,
    )


def create_409_exception(
    code: ErrorTypes, message: str, headers: dict = {}
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=ErrorResponse(msg=message, type=code).dict(),
        headers=headers,
    )


def create_401_exception(
    code: ErrorTypes, message: str, headers: dict = {}
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorResponse(msg=message, type=code).dict(),
        headers=headers,
    )


def create_403_exception(
    code: ErrorTypes, message: str, headers: dict = {}
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ErrorResponse(msg=message, type=code).dict(),
        headers=headers,
    )
