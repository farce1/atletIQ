from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import json

from app.schemas.telegram_schemas import TelegramWebhookResponse, TelegramUpdate
from app.services.telegram_service import TelegramService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/webhook", response_model=TelegramWebhookResponse)
async def telegram_webhook(request: Request):
    """
    Telegram webhook endpoint that receives messages and responds to users.
    Parses incoming Telegram updates and sends a hardcoded response message.
    """
    try:
        # Get the raw request body
        body = await request.body()
        
        # Log the received message
        logger.info("Telegram webhook triggered")
        logger.info(f"Received webhook data: {body.decode('utf-8') if body else 'Empty body'}")
        
        # Parse the incoming update
        if not body:
            logger.warning("Empty webhook body received")
            return JSONResponse(content={"message": "Empty webhook body", "success": False})
        
        try:
            update_data = json.loads(body.decode('utf-8'))
            logger.info(f"Parsed webhook JSON: {json.dumps(update_data, indent=2)}")
            
            # Parse the Telegram update
            update = TelegramUpdate(**update_data)
            
            # Check if there's a message in the update
            if update.message and update.message.text:
                chat_id = update.message.chat.id
                user_text = update.message.text
                
                logger.info(f"Received message from chat {chat_id}: {user_text}")
                
                # Initialize Telegram service
                telegram_service = TelegramService()
                
                # Send a hardcoded response message
                response_text = "Hello! I received your message. This is a hardcoded response from the bot."
                
                # Send the response
                send_result = await telegram_service.send_simple_message(chat_id, response_text)
                
                if send_result.ok:
                    logger.info(f"Successfully sent response to chat {chat_id}")
                    return JSONResponse(content={"message": "Message processed and response sent", "success": True})
                else:
                    logger.error(f"Failed to send response: {send_result.description}")
                    return JSONResponse(content={"message": "Failed to send response", "success": False})
            else:
                logger.info("No text message found in the update")
                return JSONResponse(content={"message": "No text message to process", "success": True})
                
        except json.JSONDecodeError:
            logger.error("Webhook data is not valid JSON")
            return JSONResponse(content={"message": "Invalid JSON data", "success": False})
        except Exception as parse_error:
            logger.error(f"Error parsing Telegram update: {str(parse_error)}")
            return JSONResponse(content={"message": "Error parsing update", "success": False})
        
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing Telegram webhook"
        )
