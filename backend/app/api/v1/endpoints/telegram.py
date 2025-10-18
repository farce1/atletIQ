from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import json

from app.schemas.telegram_schemas import TelegramUpdate, TelegramWebhookResponse
from app.services.telegram_handler import TelegramMessageHandler
from app.db import db_session

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/webhook", response_model=TelegramWebhookResponse)
async def telegram_webhook(request: Request):
    """
    Telegram webhook endpoint that processes both text and voice messages.
    - Text messages: Responds with text
    - Voice messages: Transcribes using ElevenLabs, processes, and responds with voice
    """
    try:
        body = await request.body()
        logger.info("Telegram webhook triggered")

        if not body:
            logger.warning("Received empty webhook body")
            return JSONResponse(content={"message": "Empty body", "success": False})

        # Parse webhook payload
        update = _parse_webhook_body(body)

        if not update.message:
            logger.info("No message in update, ignoring")
            return JSONResponse(content={"message": "No message", "success": True})

        # Ignore messages from bots (including our own responses)
        if update.message.from_.is_bot:
            logger.info(f"Ignoring message from bot: {update.message.from_.id}")
            return JSONResponse(content={"message": "Bot message ignored", "success": True})

        # Process the message
        await _process_telegram_message(update)

        return JSONResponse(content={"message": "Message processed", "success": True})

    except json.JSONDecodeError:
        logger.error("Webhook data is not valid JSON")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValueError as e:
        logger.warning(f"Value error: {str(e)}")
        return JSONResponse(content={"message": str(e), "success": True})
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Internal server error processing Telegram webhook"
        )


def _parse_webhook_body(body: bytes) -> TelegramUpdate:
    """Parse webhook body into TelegramUpdate model."""
    json_data = json.loads(body.decode('utf-8'))
    logger.info(f"Parsed webhook JSON: {json.dumps(json_data, indent=2)}")
    return TelegramUpdate(**json_data)


async def _process_telegram_message(update: TelegramUpdate) -> None:
    """Process Telegram message using the handler."""
    with db_session() as db:
        handler = TelegramMessageHandler(db=db)
        await handler.handle_message(update.message)
