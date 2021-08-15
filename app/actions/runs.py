import json
from datetime import datetime
from typing import List


from app.errors import create_400_exception
from app.errors import create_403_exception
from app.errors import create_404_exception
from app.errors import ErrorTypes
from app.apis.weather import get_weather_forecast
from app.models.db.runs import RunsModel as runs_db
from app.models.db.locations import LocationsModel as locations_db
from app.models.validators import runs as runs_validator
from app.models.validators import weather as weather_validator


async def create_run(user_id: str) -> runs_validator.RunsDB:
    has_ongoing_runs = await runs_db.has_ongoing_runs(user_id=user_id)
    if has_ongoing_runs:
        raise create_400_exception(
            ErrorTypes.USER_HAS_ONGOING_RUNS,
            "user_id {user_id} already has ongoing runs",
        )
    return await runs_db.insert_run(user_id)


async def get_runs_for_user(user_id: str, query=str) -> runs_validator.RunsReport:
    return await runs_db.get_runs(user_id=user_id, filter_query=query)


async def update_run(
    user_id: str, run: runs_validator.RunUpdate
) -> runs_validator.RunsDB:
    await raise_if_not_run_owner(run.id, user_id)

    run_dict = run.dict(exclude_unset=True)
    if "status" in run_dict and run_dict["status"] == runs_validator.RunStatus.ENDED:
        last_location = await locations_db.get_run_locations(run.id, last_n=1)
        if last_location:
            weather_json = await get_weather_forecast(
                f"{last_location[0].lat},{last_location[0].lon}"
            )
            weather_obj = weather_validator.WeatherForecastResponse(**weather_json)
            run.weather = json.dumps(weather_obj.dict(exclude_unset=True))

    return await runs_db.update_run(run)


async def update_distance(run_id: str, new_distance: float):
    run = await runs_db.get_run_by_id(run_id)
    old_distance = run.distance if run.distance else 0.0
    run.distance = old_distance + new_distance
    await runs_db.update_run(
        runs_validator.RunUpdate(**{"id": run_id, "distance": new_distance})
    )


async def update_speed(run_id):
    run = await runs_db.get_run_by_id(run_id)
    distance = run.distance if run.distance else 0.0
    time_delta = datetime.now() - run.created_at
    time_delta_hour = time_delta.microseconds / 3600000000
    if distance == 0 or time_delta_hour == 0:
        speed = 0.0
    else:
        speed = distance / time_delta_hour

    await runs_db.update_run(runs_validator.RunUpdate(**{"id": run_id, "speed": speed}))


async def validate_run_access(run_id: str, user_id: str):
    await raise_if_run_doesnt_exist(run_id)
    await raise_if_not_run_owner(run_id, user_id)
    await raise_if_not_in_progress(run_id)


async def raise_if_not_run_owner(run_id: str, user_id: str):
    run_owner = await runs_db.get_run_owner(run_id)
    if user_id != run_owner:
        raise create_403_exception(
            ErrorTypes.INVALID_TOKEN,
            f"user_id {user_id} not allowed to use this resource",
        )


async def raise_if_run_doesnt_exist(run_id: str):
    run_exists = await runs_db.run_exists(run_id)
    if not run_exists:
        raise create_404_exception(
            ErrorTypes.RUN_NOT_FOUND,
            f"run {run_id} not found",
        )


async def raise_if_not_in_progress(run_id: str):
    run = await runs_db.get_run_by_id(run_id)
    if run.status != runs_validator.RunStatus.IN_PROGRESS:
        raise create_400_exception(
            ErrorTypes.RUN_NOT_IN_PROGRESS,
            f"run {run_id} not in progress",
        )
