import uuid
import asyncio

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Table

from app import settings
from app.main import jogging_app
from app.providers import db
from app.models.db.runs import runs_table
from app.models.db.users import users_table
from app.models.db.users import agents_table
from app.models.db.users import admins_table
from app.models.db.locations import locations_table
from app.models.validators.users import UserType
from app.models.validators.users import UserSignup
from app.models.validators.locations import LocationCreateRequest
from app.actions import tokens as tokens_actions
from app.actions import users as users_actions
from app.actions import runs as runs_actions
from app.actions import locations as locations_actions


with open(settings.JWT_PRIV_KEY_PATH) as f:
    PRIV_KEY = f.read()


def block_on(future):
    return asyncio.get_event_loop().run_until_complete(future)


@pytest.fixture
def client():
    with TestClient(jogging_app) as client:
        block_on(db.execute(query=locations_table.delete()))
        block_on(db.execute(query=runs_table.delete()))
        block_on(db.execute(query=users_table.delete()))
        block_on(db.execute(query=agents_table.delete()))
        block_on(db.execute(query=admins_table.delete()))
        yield client


@pytest.fixture
def seed_users_agents_admins():
    def seed_data(count=1):
        for i in range(count):
            block_on(
                users_actions.create_user(
                    UserSignup(email=f"test{i}@test.com", password="testpass1234!"),
                    user_type=UserType.USER,
                )
            )

            block_on(
                users_actions.create_user(
                    UserSignup(email=f"test{i}@test.com", password="testpass1234!"),
                    user_type=UserType.AGENT,
                )
            )

            block_on(
                users_actions.create_user(
                    UserSignup(email=f"test{i}@test.com", password="testpass1234!"),
                    user_type=UserType.ADMIN,
                )
            )
    
    return seed_data


@pytest.fixture
def create_token():
    def make_token(exp=None, user_id="", user_type=UserType.USER.value):
        token_obj = block_on(tokens_actions.create_token(user_id, user_type))
        return token_obj.token

    return make_token


@pytest.fixture
def create_user():
    def create_new_user(email="testtest@test.com", user_type=UserType.USER):
        user = block_on(
            users_actions.create_user(
                UserSignup(email=email, password="testpass1234!"), user_type=user_type
            )
        )
        return user.id

    return create_new_user


@pytest.fixture
def create_run():
    def create_new_run(user_id):
        run = block_on(runs_actions.create_run(user_id))
        return run.id

    return create_new_run


@pytest.fixture
def add_run_locations():
    def insert_run_locations(run_id, user_id):
        block_on(
            locations_actions.create_location(
                user_id,
                LocationCreateRequest(run_id=run_id, lat=52.3845308, lon=4.9023174),
            )
        )
        block_on(
            locations_actions.create_location(
                user_id,
                LocationCreateRequest(run_id=run_id, lat=52.3861335, lon=4.8998977),
            )
        )
        block_on(
            locations_actions.create_location(
                user_id,
                LocationCreateRequest(run_id=run_id, lat=52.3877248, lon=4.8999436),
            )
        )

    return insert_run_locations


@pytest.fixture
def mock_weather_api(mocker):
    def mock_api(
        response, side_effect=None,
    ):
        future = asyncio.Future()
        future.set_result(response)
        mock = mocker.patch(
            "app.apis.weather.get_weather_forecast",
            return_value=future,
            side_effect=side_effect,
        )
        return mock

    return mock_api

