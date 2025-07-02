import databases
import sqlalchemy
from app.config.config import settings

DATABASE_URL = settings.db_url

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)