from fastapi import APIRouter, Request, Response, status
import json

from app.bot import client, BASE_URL, logger

bot_router = APIRouter(prefix="/bot", tags=["bot"])

@bot_router.post("/webhook/")
async def webhook(req: Request):
    body_bytes = await req.body()
    text_body = body_bytes.decode(errors="ignore")
    logger.info("Incoming webhook: %s", text_body)

    if not text_body:
        return Response(status_code=status.HTTP_200_OK)

    try:
        data = json.loads(text_body)
    except json.JSONDecodeError:
        logger.error("JSON decode error")
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    message = data.get("message")
    if not message or "text" not in message:
        return Response(status_code=status.HTTP_200_OK)

    chat_id = message["chat"]["id"]
    text = message["text"]

    resp = await client.get(
        f"{BASE_URL}/sendMessage",
        params={"chat_id": chat_id, "text": text}
    )
    logger.info("sendMessage response: %s", resp.text)

    return {"ok": True}