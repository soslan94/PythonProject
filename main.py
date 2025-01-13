from contextlib import asynccontextmanager

import databases
import sqlalchemy
from fastapi import FastAPI
from starlette.requests import Request

from decouple import config

DATABASE_URL = (
    f'postgresql://{config("DB_USER")}:'
    f'{config("DB_PASSWORD")}@'
    f'{config("DB_HOST")}:'
    f'{config("DB_PORT")}/'
    f'{config("DB_NAME")}'
)


database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('author', sqlalchemy.String),
    sqlalchemy.Column('pages', sqlalchemy.INTEGER),
    sqlalchemy.Column('reader_id', sqlalchemy.ForeignKey('readers.id'), index=True),
)

readers = sqlalchemy.Table(
    "readers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('first_name', sqlalchemy.String),
    sqlalchemy.Column('last_name', sqlalchemy.String),
)


readers_books = sqlalchemy.Table(
    "readers_books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('book_id', sqlalchemy.ForeignKey('books.id'), nullable=False),
    sqlalchemy.Column('reader_id', sqlalchemy.ForeignKey('readers.id'), nullable=False),
)

#app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Application is starting")
    yield
    await database.disconnect()
    print("Application is shutting down")

app = FastAPI(lifespan=lifespan)

@app.get('/books/')
async def get_all_books():
    query = books.select()
    return await database.fetch_all(query)

@app.post('/books/')
async def create_book(request: Request):
    data = await request.json()
    query = books.insert().values(**data)
    last_record_id = await database.execute(query)
    return {'id': last_record_id}


@app.post('/readers/')
async def create_reader(request: Request):
    data = await request.json()
    query = readers.insert().values(**data)
    last_record_id = await database.execute(query)
    return {'id': last_record_id}

@app.post('/readers_books/')
async def create_readers_books(request: Request):
    data = await request.json()
    query = readers_books.insert().values(**data)
    last_record_id = await database.execute(query)
    return {'id': last_record_id}
