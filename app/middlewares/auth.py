import logging
from typing import FrozenSet

import jwt
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from app import settings
from app.errors import create_403_exception
from app.errors import ErrorTypes

with open(settings.JWT_PUB_KEY_PATH) as f:
    PUB_KEY = f.read()



class VerifyUserToken:
    def __init__(self, scopes: FrozenSet[str]):
        self.scopes = scopes

    async def __call__(
        self, creds: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ):

        try:
            token = creds.credentials
            decoded = jwt.decode(token, PUB_KEY, algorithms=settings.JWT_ALGO,)
            uid = decoded["uid"]
            scopes = decoded["scopes"]
            user_type = decoded["user_type"]
            for s in self.scopes:
                if s not in scopes:
                    logging.warning(
                        f"Required scope {s} not found for user {uid}",
                    )
                    raise create_403_exception(
                        ErrorTypes.REQUIRED_SCOPE_NOT_FOUND,
                        f"Required scope {s} not found",
                    )

            return {"user_id": uid, "user_type": user_type}

        except jwt.exceptions.InvalidSignatureError:
            logging.warning("Invalid token signature")
            raise create_403_exception(ErrorTypes.INVALID_TOKEN, "")

        except (
            ValueError,
            jwt.exceptions.DecodeError,
            jwt.exceptions.InvalidTokenError,
            jwt.exceptions.InvalidKeyError,
            jwt.exceptions.ExpiredSignatureError
        ) as e:
            logging.warning(f"Invalid token {e}")
            raise create_403_exception(ErrorTypes.INVALID_TOKEN, "")


check_user_perm = VerifyUserToken(["runs", "locations"])
check_agent_perm = VerifyUserToken(["users", "runs", "locations"])
check_admin_perm = VerifyUserToken(["admins", "agents", "runs", "locations"])
