import uuid
from typing import List

from pydantic import parse_obj_as
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func

from app.providers import db
from app.providers import metadata
from app.models.validators import locations as locations_validators


locations_table = Table(
    "locations",
    metadata,
    Column("id", String, nullable=False, primary_key=True),
    Column("run_id", ForeignKey("runs.id"), nullable=False),
    Column("lat", Float, nullable=False),
    Column("lon", Float, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)

# This is used when fetching all columns
locations_table_cols = [c for c in locations_table.c]


class LocationsModel:
    @staticmethod
    async def insert_location(
        location: locations_validators.LocationCreateRequest,
    ) -> locations_validators.LocationDB:
        uid = str(uuid.uuid4())
        query = locations_table.insert().returning(*locations_table_cols)
        location = location.dict()
        location["id"] = uid

        created_location = await db.fetch_one(query=query, values=location)

        created_location = locations_validators.LocationDB(
            **created_location, exclude_unset=True
        )
        return created_location

    @staticmethod
    async def get_run_locations(
        run_id: str, last_n: int = 2
    ) -> List[locations_validators.LocationDB]:

        query = locations_table.select().where(locations_table.c.run_id == run_id)

        run_locations = await db.fetch_all(query=query)
        run_locations = run_locations[-last_n:] if last_n else run_locations
        return parse_obj_as(List[locations_validators.LocationDB], run_locations)
