import json
from datetime import datetime


from app import errors
from app.apis.weather import get_weather_forecast
from app.models.db.runs import RunsModel as runs_db
from app.models.db.locations import LocationsModel as locations_db
from app.models.validators import runs as runs_validator
from app.models.validators import locations as locations_validator
from app.models.validators import weather as weather_validator

MICROS_TO_HOURS = 3600000000


async def create_run(user_id: str) -> runs_validator.RunsDB:
    """Create a new run for a user if she doesnt have an existing ongoing run"""
    has_ongoing_runs = await runs_db.has_ongoing_runs(user_id=user_id)
    if has_ongoing_runs:
        raise errors.create_400_exception(
            errors.ErrorTypes.USER_HAS_ONGOING_RUNS,
            f"user_id {user_id} already has ongoing runs",
        )
    return await runs_db.insert_run(user_id)


async def get_runs(user_id: str, query=str) -> runs_validator.RunsReport:
    """Get all runs for a user as a report"""
    return await runs_db.get_runs(user_id=user_id, filter_query=query)


async def update_run(
    user_id: str, run: runs_validator.RunUpdate
) -> runs_validator.RunsDB:
    """
    Update run for a user
    if shes the owner, otherwise raise a 403
    save weather forecast if the run has ended
    """
    await raise_if_not_run_owner(run.id, user_id)

    run_dict = run.dict(exclude_unset=True)

    if "status" in run_dict and run_dict["status"] == runs_validator.RunStatus.ENDED:
        last_location = await locations_db.get_run_locations(run.id, last_n=1)
        if last_location:
            run.weather = await weather_forecast_as_json(last_location=last_location[0])

    return await runs_db.update_run(run)


async def weather_forecast_as_json(
    last_location: locations_validator.LocationDB,
) -> str:
    """
    Get weather forecast through external api
    trim fields by applying the validator model
    convert back to json to be saved in the db
    """
    weather_json = await get_weather_forecast(
        f"{last_location.lat},{last_location.lon}"
    )
    weather_obj = weather_validator.WeatherForecastResponse(**weather_json)
    return json.dumps(weather_obj.dict(exclude_unset=True))


async def validate_run_access(run_id: str, user_id: str):
    """apply validation checks to update locations of a run"""
    await raise_if_run_doesnt_exist(run_id)
    await raise_if_not_run_owner(run_id, user_id)
    await raise_if_not_in_progress(run_id)


async def raise_if_not_run_owner(run_id: str, user_id: str):
    run_owner = await runs_db.get_run_owner(run_id)
    if user_id != run_owner:
        raise errors.create_403_exception(
            errors.ErrorTypes.INVALID_TOKEN,
            f"user_id {user_id} not allowed to use this resource",
        )


async def raise_if_run_doesnt_exist(run_id: str):
    run_exists = await runs_db.run_exists(run_id)
    if not run_exists:
        raise errors.create_404_exception(
            errors.ErrorTypes.RUN_NOT_FOUND,
            f"run {run_id} not found",
        )


async def raise_if_not_in_progress(run_id: str):
    run = await runs_db.get_run_by_id(run_id)
    if run.status != runs_validator.RunStatus.IN_PROGRESS:
        raise errors.create_400_exception(
            errors.ErrorTypes.RUN_NOT_IN_PROGRESS,
            f"run {run_id} not in progress",
        )


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
    time_delta_hour = time_delta.microseconds / MICROS_TO_HOURS
    if distance == 0 or time_delta_hour == 0:
        speed = 0.0
    else:
        speed = distance / time_delta_hour

    await runs_db.update_run(runs_validator.RunUpdate(**{"id": run_id, "speed": speed}))
