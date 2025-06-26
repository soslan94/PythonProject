from fastapi import FastAPI
from .db import database
from .routers import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def on_startup():
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()