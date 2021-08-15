import logging
from typing import List
from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from app.actions import users as users_actions
from app.models.validators import users as users_validator
from app.middlewares.auth import check_agent_perm
from app.errors import create_403_exception
from app.errors import ErrorTypes

router = APIRouter()


def validate_agent_token(user_token_data: Dict = Depends(check_agent_perm)):
    user_type = user_token_data["user_type"]
    user_id = user_token_data["user_id"]

    if user_type != "AGENT":
        raise create_403_exception(
            ErrorTypes.REQUIRED_SCOPE_NOT_FOUND, f"user {user_id} is not agent",
        )
    return user_token_data


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=users_validator.UsersPaginate,
)
async def get_users(
    page: int = 1,
    page_count: int = 10,
    user_token_data: Dict = Depends(validate_agent_token)
):
    user_type = user_token_data["user_type"]
    user_id = user_token_data["user_id"]

    logging.info(f"Listing all users for {user_type} {user_id}")
    return await users_actions.get_users(user_type=users_validator.UserType.USER, page=page, page_count=page_count)


@router.post(
    "/users", status_code=status.HTTP_200_OK,
)
async def create_user(
    credentials: users_validator.UserSignup,
    user_token_data: Dict = Depends(validate_agent_token),
):
    user_type = user_token_data["user_type"]
    user_id = user_token_data["user_id"]

    logging.info(f"{user_type} with id {user_id} creating a new user")
    return await users_actions.create_user(
        credentials=credentials, user_type=users_validator.UserType.USER
    )

