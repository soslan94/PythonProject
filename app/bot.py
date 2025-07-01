import os
import logging
import httpx

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("uvicorn.error")

TOKEN = os.getenv("TELEGRAM_TOKEN")
NGROK_URL = os.getenv("NGROK_URL", "").rstrip("/")
WEBHOOK_URL = f"{NGROK_URL}/bot/webhook/"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

client: httpx.AsyncClient = httpx.AsyncClient(timeout=10.0)