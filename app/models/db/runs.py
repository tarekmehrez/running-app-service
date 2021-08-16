from logging import error
import uuid
from typing import List

import pandas as pd
from pydantic import parse_obj_as
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy import func
from sqlalchemy import desc

from app import errors
from app.providers import db
from app.providers import metadata
from app.models.validators import runs as runs_validator

runs_table = Table(
    "runs",
    metadata,
    Column("id", String, nullable=False, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("status", String, nullable=False),
    Column("description", String, nullable=True),
    Column("distance", Float, nullable=True),
    Column("speed", Float, nullable=True),
    Column("weather", JSON, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now()),
)

# This is used when fetching all columns
runs_table_cols = [c for c in runs_table.c]


class RunsModel:
    @staticmethod
    async def insert_run(user_id: str) -> runs_validator.RunsDB:
        """
        create new uid
        insert new run with status in progress
        """
        uid = str(uuid.uuid4())
        query = runs_table.insert().returning(*runs_table_cols)
        run = {
            "id": uid,
            "status": runs_validator.RunStatus.IN_PROGRESS,
            "user_id": user_id,
        }

        created_run = await db.fetch_one(query=query, values=run)

        created_run = runs_validator.RunsDB(**created_run, exclude_unset=True)
        return created_run

    @staticmethod
    async def update_run(run: runs_validator.RunUpdate) -> runs_validator.RunsDB:
        """
        exclude id, that wont be updated
        update run with new values
        """
        query = (
            runs_table.update()
            .where(runs_table.c.id == run.id)
            .values(**run.dict(exclude={"id"}, exclude_unset=True))
            .returning(*runs_table_cols)
        )
        updated_run = await db.fetch_one(query=query)
        updated_run = runs_validator.RunsDB(**updated_run, exclude_unset=True)
        return updated_run

    @staticmethod
    async def get_runs(
        user_id: str, filter_query: str = "", summary: bool = True
    ) -> runs_validator.RunsReport:
        """
        all get run requests return a report at this point
        a report is a list of runs with a summary
        a summary is basic stats on distance and speed
        a query can be applied to filter the returned runs for any given field

        querying is done through pandas query function
        """
        # get runs from the database
        query = (
            runs_table.select()
            .order_by(desc(runs_table.c.created_at))
            .where(runs_table.c.user_id == user_id)
        )
        user_runs = await db.fetch_all(query=query)
        runs_df = pd.DataFrame.from_records(user_runs)

        # filter based on user's query
        if filter_query:
            try:
                runs_df = runs_df.query(filter_query)
            except Exception as e:
                raise errors.create_400_exception(
                    errors.ErrorTypes.BAD_QUERY,
                    f"bad query: {e}",
                )

        runs_dict = runs_df.to_dict(orient="records")
        runs_obj = parse_obj_as(List[runs_validator.RunsDB], runs_dict)

        result = runs_validator.RunsReport(runs=runs_obj)

        # get summary of selected runs
        if not runs_df.empty and summary:
            summary_dict = (
                runs_df[["distance", "speed"]].describe(include="all").to_dict()
            )
            summary_obj = runs_validator.RunsSummary(**summary_dict)
            result.summary = summary_obj

        return result

    @staticmethod
    async def get_run_owner(run_id: str) -> str:
        """get user id of a run"""
        query = runs_table.select().where(runs_table.c.id == run_id)
        run = await db.fetch_one(query=query)
        return run["user_id"]

    @staticmethod
    async def has_ongoing_runs(user_id: str) -> bool:
        """check if the user has runs with status in progress"""
        query = (
            runs_table.select()
            .order_by(desc(runs_table.c.created_at))
            .where(runs_table.c.user_id == user_id)
            .where(runs_table.c.status == runs_validator.RunStatus.IN_PROGRESS)
        )
        user_run = await db.fetch_one(query=query)
        return user_run is not None

    @staticmethod
    async def run_exists(run_id: str) -> bool:
        """check if run id exists"""
        query = runs_table.select().where(runs_table.c.id == run_id)
        run = await db.fetch_one(query=query)
        return run is not None

    @staticmethod
    async def get_run_by_id(run_id: str) -> runs_validator.RunsDB:
        """return run record for a specific id"""
        query = runs_table.select().where(runs_table.c.id == run_id)
        run = await db.fetch_one(query=query)
        return runs_validator.RunsDB(**run)
