import json
import jwt
import logging
from datetime import datetime
from datetime import timedelta

from app import settings
from app.models.validators import users as users_validator


SECONDS_PER_UNIT = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

with open(settings.JWT_PRIV_KEY_PATH) as f:
    PRIV_KEY = f.read()

with open(settings.SCOPES_CONFIG_PATH) as f:
    TOKEN_SCOPES = json.load(f)


async def create_token(
    user_id: str, user_type: users_validator.UserType
) -> users_validator.AuthToken:
    token_payload = await generate_token_payload(user_type=user_type)
    token_payload["uid"] = user_id

    token = await sign_token(token_payload)
    return users_validator.AuthToken(token=token)


async def generate_token_payload(user_type: users_validator.UserType) -> dict:

    values = TOKEN_SCOPES[user_type]
    expiry = values["expiry"]

    expiry_seconds = int(expiry[0]) * int(SECONDS_PER_UNIT[expiry[-1]])
    expiry_timestamp = (datetime.now() + timedelta(seconds=expiry_seconds)).timestamp()

    return {"scopes": values["scopes"], "exp": expiry_timestamp, "user_type": user_type}


async def sign_token(payload: dict) -> str:

    try:
        token = jwt.encode(payload, PRIV_KEY, algorithm=settings.JWT_ALGO)
        return token
    except Exception as e:
        logging.error(f"Failed creating token for user {e}")
        raise e

