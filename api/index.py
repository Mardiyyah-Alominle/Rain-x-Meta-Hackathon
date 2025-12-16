import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Import Config
from config import Config

# Import your compiled LangGraph application
from workflows.shop_flow import app as shop_app
# Import DB init to ensure mock data/firebase loads on startup
from utils.db import db

# Import new API routers
from api.products_api import router as products_router
from api.sales_api import router as sales_router
from api.analytics_api import router as analytics_router

# Load environment variables
load_dotenv()

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup FastAPI
app = FastAPI(
    title="AestheticBot API",
    description="E-commerce chatbot API with admin dashboard endpoints",
    version="1.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
        # Add your production frontend URL here when deployed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(products_router)
app.include_router(sales_router)
app.include_router(analytics_router)

# Telegram API Setup
TELEGRAM_BOT_TOKEN = Config.TELEGRAM_BOT_TOKEN
if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set in configuration!")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# --- Helper Function to reply to Telegram ---
async def send_telegram_message(chat_id: int, text: str):
    """Sends a text message back to a specific Telegram chat."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json={"chat_id": chat_id, "text": text},
                timeout=10.0
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send message to Telegram: {e}")


# --- The Main Webhook Endpoint ---
@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    """
    This is the URL that Telegram calls whenever your bot receives a message.
    """
    try:
        # 1. Parse the incoming JSON update from Telegram
        update = await request.json()
        logger.info(f"Received update: {update}")

        # 2. Basic Validation (Deterministically ignore non-message updates)
        # If it doesn't have a 'message' or text content, just acknowledge and ignore.
        if "message" not in update or "text" not in update["message"]:
            return Response(status_code=200)

        message_data = update["message"]
        chat_id = message_data["chat"]["id"]
        incoming_text = message_data["text"]
        user_id_str = str(chat_id)

        # 3. Prepare Input for LangGraph
        # We need to maintain state per user. The 'thread_id' config is crucial here.
        # We use the Telegram chat_id as the thread_id to isolate sessions.
        config = {"configurable": {"thread_id": user_id_str}}

        # Define the input state needed for the graph
        inputs = {
            # The new message from the user
            "messages": [HumanMessage(content=incoming_text)],
            # Ensure customer_id is in state for the Fulfillment Agent to use later
            "customer_id": user_id_str
        }

        # 4. Run the AI Workflow
        # We use .ainvoke() to run the graph asynchronously.
        # LangGraph handles running the agents and tools based on the workflow definition.
        final_state = await shop_app.ainvoke(inputs, config=config)

        # 5. Extract the Final Response
        # Look at the last message in the final state history.
        last_message = final_state["messages"][-1]
        response_text = last_message.content

        # Safety check: If the AI tried to call a tool but didn't generate text,
        # provide a default fallback message.
        if not response_text:
            response_text = "Hold on, let me process that..."

        # 6. Send the reply back to Telegram
        await send_telegram_message(chat_id, response_text)

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        # Even on error, return 200 OK to Telegram so it stops retrying.
        # In a real app, you might send an error message back to the user.
        return Response(status_code=200)

    # Return 200 OK to acknowledge receipt to Telegram
    return Response(status_code=200)


# --- Health Check Endpoint ---
@app.get("/")
async def health_check():
    return {"status": "AestheticBot is running!", "db_status": "Mock DB Active" if db is None else "Firebase Connected"}