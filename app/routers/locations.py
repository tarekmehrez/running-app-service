import logging
from typing import List
from typing import Dict

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from app.actions import locations as locations_actions
from app.models.validators import locations as locations_validators
from app.middlewares.auth import check_user_perm


router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=locations_validators.LocationDB,
)
async def add_location(
    location: locations_validators.LocationCreateRequest,
    user_token_data: Dict = Depends(check_user_perm),
):
    user_id = user_token_data["user_id"]
    logging.info(f"Creating a new location for run {location.run_id}")
    return await locations_actions.create_location(user_id=user_id, location=location)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[locations_validators.LocationDB],
)
async def get_runs_locations(
    run_id: str,
    user_token_data: Dict = Depends(check_user_perm),
):
    user_id = user_token_data["user_id"]
    logging.info(f"Getting all locations for run {run_id}")
    return await locations_actions.get_run_locations(user_id=user_id, run_id=run_id)
