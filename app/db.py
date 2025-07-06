import databases
import sqlalchemy
from app.settings import settings

DATABASE_URL = settings.POSTGRES.db_url

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)