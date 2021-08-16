import logging
from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends

from app.apis import weather as weather_api
from app.models.validators import weather as weather_validators
from app.middlewares.auth import check_user_perm

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_weather_forecast(
    lat: float,
    lon: float,
    user_id: str = Depends(check_user_perm),
):
    logging.info(f"Getting weather forecast for user {user_id}")
    forecast = await weather_api.get_weather_forecast(query=f"{lat},{lon}")
    return weather_validators.WeatherForecastResponse(**forecast)
