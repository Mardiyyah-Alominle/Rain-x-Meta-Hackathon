import os
from dotenv import load_dotenv

# Load the .env file immediately
load_dotenv()

class Config:
    # LLM Provider (Groq)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Telegram Bot API
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Firebase Admin SDK Credentials
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY")
    FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")

    # Model Name (You can add this back if you have a specific model in mind,
    # otherwise it's not strictly in the .env you provided, but is in the source examples)
    MODEL_NAME = "llama-3.3-70b-versatile"