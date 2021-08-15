from databases import Database
from sqlalchemy import MetaData

from app import settings

metadata = MetaData()
db = Database(settings.DATABASE_URI)
