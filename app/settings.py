import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(os.getenv("ENV_PATH", ".")) / ".env"
load_dotenv(dotenv_path=env_path)

ENV = os.getenv("ENV", "dev")
DOCS_PREFIX = os.getenv("DOCS_PREFIX", "")

JWT_ALGO = os.getenv("JWT_ALGO", "RS256")
SCOPES_CONFIG_PATH = os.getenv("SCOPES_CONFIG", "./scopes.json")
JWT_PRIV_KEY_PATH = os.getenv("JWT_PRIV_KEY_PATH", "./jwt-key")
JWT_PUB_KEY_PATH = os.getenv("JWT_PUB_KEY_PATH", "./jwt-key.pub")


# DATABASE
DATABASE_HOST = os.getenv("DATABASE_HOST", "127.0.0.1")
DATABASE_PORT = os.getenv("DATABASE_PORT", 5432)
DATABASE_NAME = os.getenv("DATABASE_NAME", "postgres")
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgrespass")
DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


WEATHER_API_URI = os.getenv(
    "WEATHER_API_URI", "http://api.weatherapi.com/v1/current.json"
)
WEATHER_API_TOKEN = os.getenv("WEATHER_API_TOKEN", "e742048f344f437297e190130211208")
