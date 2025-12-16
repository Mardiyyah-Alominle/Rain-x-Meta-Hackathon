"""
Test if your .env file is correctly formatted
"""
import os
from dotenv import load_dotenv

print("=" * 60)
print("Testing .env File")
print("=" * 60)

# Load .env file
load_dotenv()

# Check each variable
variables = {
    "FIREBASE_PROJECT_ID": os.getenv("FIREBASE_PROJECT_ID"),
    "FIREBASE_CLIENT_EMAIL": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "FIREBASE_PRIVATE_KEY": os.getenv("FIREBASE_PRIVATE_KEY"),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
}

print("\n✅ Variables loaded from .env:\n")

for key, value in variables.items():
    if value:
        # Show first 50 chars for security
        display_value = value[:50] + "..." if len(value) > 50 else value
        print(f"  {key}: {display_value}")
    else:
        print(f"  ❌ {key}: NOT SET")

print("\n" + "=" * 60)

# Check Firebase variables specifically
firebase_vars = ["FIREBASE_PROJECT_ID", "FIREBASE_CLIENT_EMAIL", "FIREBASE_PRIVATE_KEY"]
missing = [var for var in firebase_vars if not variables[var]]

if missing:
    print(f"\n❌ Missing Firebase variables: {', '.join(missing)}")
    print("\nYour .env file is incomplete or has formatting errors.")
    print("Please check lines 13-14 mentioned in the error.")
else:
    print("\n✅ All Firebase variables are set!")
    print("\nNow testing Firebase initialization...")
    
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        if not firebase_admin._apps:
            # Format the private key
            private_key = variables["FIREBASE_PRIVATE_KEY"]
            formatted_key = private_key.replace('\\n', '\n')
            
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": variables["FIREBASE_PROJECT_ID"],
                "private_key": formatted_key,
                "client_email": variables["FIREBASE_CLIENT_EMAIL"],
            })
            
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            
            print("✅ Firebase initialized successfully!")
            print("\nYour .env file is correctly formatted!")
            
    except Exception as e:
        print(f"\n❌ Firebase initialization failed: {e}")
        print("\nThis means your credentials are loaded but invalid.")
        print("Please check:")
        print("  1. The private key is correct")
        print("  2. The project ID matches your Firebase project")
        print("  3. The client email is correct")

print("\n" + "=" * 60)
