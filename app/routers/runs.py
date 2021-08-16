import logging
from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from app.actions import runs as runs_actions
from app.models.validators import runs as runs_validator
from app.middlewares.auth import check_user_perm

router = APIRouter()


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=runs_validator.RunsDB
)
async def create_run(user_token_data: Dict = Depends(check_user_perm)):
    user_id = user_token_data["user_id"]
    logging.info(f"Creating a new run for user {user_id}")
    return await runs_actions.create_run(user_id=user_id)


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=runs_validator.RunsReport
)
async def get_runs(query: str = None, user_token_data: Dict = Depends(check_user_perm)):
    user_id = user_token_data["user_id"]
    logging.info(f"Getting all runs for user {user_id} with query {query}")
    return await runs_actions.get_runs(user_id=user_id, query=query)


@router.patch("", status_code=status.HTTP_200_OK, response_model=runs_validator.RunsDB)
async def patch_run(
    run: runs_validator.RunUpdate, user_token_data: Dict = Depends(check_user_perm)
):
    user_id = user_token_data["user_id"]
    logging.info(f"Updating run {run.id} for user {user_id}")
    return await runs_actions.update_run(user_id=user_id, run=run)
