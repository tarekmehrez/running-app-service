import logging

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError

from app import settings
from app.errors import create_400_exception
from app.errors import ErrorTypes


async def get_weather_forecast(query: str):
    try:
        async with ClientSession() as session:
            url = (
                f"{settings.WEATHER_API_URI}?key={settings.WEATHER_API_TOKEN}&q={query}"
            )
            response = await session.request(method="GET", url=url)
            response.raise_for_status()
            response_json = await response.json()

            return response_json

    except ClientResponseError as err:
        logging.error(
            "Error occurred while requesting weather conditions for query {query}",
        )
        raise create_400_exception(ErrorTypes.BAD_REQUEST, message=str(err))
