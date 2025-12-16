import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables from .env file immediately
load_dotenv()

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK securely using environment variables.
    Returns the Firestore client object for database access.
    """
    # Prevent double-initialization errors if the app reloads (common in development)
    if not firebase_admin._apps:
        try:
            print("Attempting to initialize Firebase...")

            # 1. Fetch credentials from environment variables
            project_id = os.getenv("FIREBASE_PROJECT_ID")
            private_key = os.getenv("FIREBASE_PRIVATE_KEY")
            client_email = os.getenv("FIREBASE_CLIENT_EMAIL")

            # Basic validation
            if not all([project_id, private_key, client_email]):
                raise ValueError("Error: Missing one or more required Firebase environment variables (PROJECT_ID, PRIVATE_KEY, or CLIENT_EMAIL).")

            # 2. CRITICAL FIX FOR VERCEL/ENV VARS
            # When storing multi-line private keys in environment variables (like on Vercel),
            # newlines ('\n') are often escaped as literal backslash-n ('\\n').
            # We must replace them back to actual newlines for the certificate to work.
            formatted_private_key = private_key.replace('\\n', '\n')

            # 3. Create credentials object dynamically
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": project_id,
                "private_key": formatted_private_key,
                "client_email": client_email,
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            })

            # 4. Initialize the App
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin SDK initialized successfully.")

        except Exception as e:
            print(f"🔥 CRITICAL ERROR initializing Firebase: {e}")
            # In a real deployment, you might want to raise this to prevent the app from starting improperly.
            # raise e
            return None

    # Return the Firestore client
    return firestore.client()

# Initialize the database connection globally.
# Other files can now import this 'db' object.
db = initialize_firebase()