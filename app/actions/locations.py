from typing import List

from app.actions import runs as runs_actions
from app.actions import utils
from app.models.db.locations import LocationsModel as locations_db
from app.models.validators import locations as locations_validators


async def create_location(
    user_id: str, location: locations_validators.LocationCreateRequest
) -> locations_validators.LocationDB:
    """
    Add a new location to the run
    Check if the run has more than 1 location already, calculate distance for the last two locations
    Add the new distance to the run
    """
    await runs_actions.validate_run_access(location.run_id, user_id)
    location = await locations_db.insert_location(location)

    last_two_locations = await locations_db.get_run_locations(location.run_id, last_n=2)
    if len(last_two_locations) == 2:
        distance = await utils.haversine_distance_km(
            lat1=last_two_locations[0].lat,
            lon1=last_two_locations[0].lon,
            lat2=last_two_locations[1].lat,
            lon2=last_two_locations[1].lon,
        )
        await runs_actions.update_distance(
            run_id=location.run_id, new_distance=distance
        )
        await runs_actions.update_speed(run_id=location.run_id)
    return location


async def get_run_locations(
    user_id, run_id: str
) -> List[locations_validators.LocationDB]:
    await runs_actions.validate_run_access(run_id, user_id)
    return await locations_db.get_run_locations(run_id)
