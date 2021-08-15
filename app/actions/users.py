import logging

from fastapi import Depends
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app import errors
from app.models.validators import users as users_validator
from app.models.db.users import UserModel as users_db
from app.actions import tokens as tokens_actions

password_hasher = PasswordHasher(
    time_cost=4, memory_cost=1024 * 100, parallelism=8, hash_len=32, salt_len=16
)


async def get_user(user_type: users_validator.UserType, **kwargs):
    user = await users_db.get(user_type=user_type, **kwargs)
    if not user:
        raise errors.create_404_exception(
            code=errors.ErrorTypes.USER_NOT_FOUND, message="User not found"
        )
    return user


async def create_user(
    credentials: users_validator.UserSignup, user_type: users_validator.UserType
):
    user = await users_db.get(user_type=user_type, email=credentials.email)

    if user:
        raise errors.create_409_exception(
            code=errors.ErrorTypes.EMAIL_EXISTS,
            message="User email already exists for user",
        )

    credentials.password = password_hasher.hash(credentials.password)
    user = await users_db.insert(credentials, user_type=user_type)

    return user


async def create_user_token(
    credentials: users_validator.UserLogin, user_type: users_validator.UserType
) -> users_validator.AuthToken:
    user = await users_db.get(user_type=user_type, email=credentials.email)
    if not user:
        raise errors.create_404_exception(
            code=errors.ErrorTypes.USER_NOT_FOUND, message="User not found"
        )

    try:
        password_hasher.verify(user.password, credentials.password)
    except VerifyMismatchError as e:
        logging.error(f"cannot login for user {user.id} incorrect password")
        raise errors.create_401_exception(
            code=errors.ErrorTypes.INCORRECT_PASSWORD, message="Incorrect Password"
        )

    return await tokens_actions.create_token(user.id, user_type)


async def get_users(
    user_type: users_validator.UserType, page: int, page_count: int
) -> users_validator.UsersPaginate:
    return await users_db.list(user_type=user_type, page=page, page_count=page_count)
