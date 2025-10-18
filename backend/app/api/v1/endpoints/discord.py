from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import json

from app.schemas.discord_schemas import DiscordWebhookResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/webhook", response_model=DiscordWebhookResponse)
async def discord_webhook(request: Request):
    """
    Discord webhook endpoint that receives information when a new chat is created.
    For now, it just logs the information and returns a success message.
    """
    try:
        # Get the raw request body
        body = await request.body()
        
        # Log the received message
        logger.info("Discord webhook triggered - new chat created")
        logger.info(f"Received webhook data: {body.decode('utf-8') if body else 'Empty body'}")
        
        # Try to parse and log as JSON if possible
        try:
            if body:
                json_data = json.loads(body.decode('utf-8'))
                logger.info(f"Parsed webhook JSON: {json.dumps(json_data, indent=2)}")
        except json.JSONDecodeError:
            logger.info("Webhook data is not valid JSON, logging as raw text")
        
        # Log headers for debugging
        logger.info(f"Webhook headers: {dict(request.headers)}")
        
        return JSONResponse(content={"message": "Webhook received", "success": True})
        
    except Exception as e:
        logger.error(f"Error processing Discord webhook: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing Discord webhook"
        )
