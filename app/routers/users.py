import logging

from fastapi import APIRouter
from fastapi import status


from app.models.validators import users as users_validator
from app.actions import users as users_actions

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(credentials: users_validator.UserSignup):
    logging.info(f"Creating a new user with email {credentials.email}")
    await users_actions.create_user(
        credentials=credentials, user_type=users_validator.UserType.USER
    )


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=users_validator.AuthToken
)
async def create_user_token(credentials: users_validator.UserLogin):
    logging.info(f"Creating a new token for user with email {credentials.email}")
    return await users_actions.create_user_token(
        credentials=credentials, user_type=users_validator.UserType.USER
    )
