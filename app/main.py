import logging

from fastapi import FastAPI
from dotenv import load_dotenv

from app.db import database
from app.bot import BASE_URL, WEBHOOK_URL, client
from app.routers import router
from app.crud.crud_bot import bot_router

load_dotenv()

logger = logging.getLogger("uvicorn.error")

app = FastAPI()
app.include_router(router)
app.include_router(bot_router)

@app.on_event("startup")
async def on_startup():
    await database.connect()
    logger.info("Database connected")

    resp = await client.get(
        f"{BASE_URL}/setWebhook",
        params={"url": WEBHOOK_URL}
    )
    logger.info("setWebhook response: %s", resp.text)

    info = await client.get(f"{BASE_URL}/getWebhookInfo")
    logger.info("getWebhookInfo: %s", info.text)