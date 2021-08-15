import logging

from fastapi import FastAPI
from fastapi import status

from app import routers
from app import settings
from app.providers import db

logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=logging.INFO
)


class AppSettings:
    api_name: str = str(__name__)


config = AppSettings()

jogging_app = FastAPI(
    title="Assets Service", version="1.0.0", root_path=settings.DOCS_PREFIX,
)


@jogging_app.on_event("startup")
async def startup():
    await db.connect()


@jogging_app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@jogging_app.get("/healthz", status_code=status.HTTP_200_OK, tags=["status"])
def health():
    logging.info("Health check")
    return


jogging_app.include_router(
    routers.users, prefix="/users", tags=["users"],
)


jogging_app.include_router(
    routers.runs, prefix="/runs", tags=["runs"],
)

jogging_app.include_router(
    routers.weather, prefix="/weather", tags=["weather"],
)

jogging_app.include_router(
    routers.locations, prefix="/locations", tags=["locations"],
)

jogging_app.include_router(
    routers.admins, prefix="/admins", tags=["admins"],
)

jogging_app.include_router(
    routers.agents, prefix="/agents", tags=["agents"],
)
