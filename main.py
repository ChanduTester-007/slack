import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Slack credentials from environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

# Initialize Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Define request model
class SlackMessage(BaseModel):
    message: str
    channel: str = SLACK_CHANNEL  # Default channel if not provided

# API endpoint to send messages to Slack
@app.post("/send-message/")
async def send_message(payload: SlackMessage):
    try:
        response = client.chat_postMessage(channel=payload.channel, text=payload.message)
        logger.info(f"Message sent to {payload.channel}: {response['message']['text']}")
        return {"status": "success", "channel": payload.channel, "message": payload.message}
    except SlackApiError as e:
        logger.error(f"Error sending message: {e.response['error']}")
        raise HTTPException(status_code=400, detail=f"Slack API error: {e.response['error']}")

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "running", "message": "Slack API is live!"}