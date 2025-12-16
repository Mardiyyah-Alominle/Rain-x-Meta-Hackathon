"""
Firebase .env File Generator

This script helps you create a properly formatted .env file from your Firebase JSON credentials.
"""

import json
import sys

def create_env_file():
    print("=" * 60)
    print("Firebase .env File Generator")
    print("=" * 60)
    print()
    
    # Ask for the JSON file path
    json_path = input("Enter the path to your Firebase JSON file (or press Enter to input values manually): ").strip()
    
    if json_path:
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            project_id = data.get('project_id', '')
            client_email = data.get('client_email', '')
            private_key = data.get('private_key', '')
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            print("Please enter values manually instead.")
            return manual_input()
    else:
        return manual_input()
    
    # Get other credentials
    print("\nOptional credentials (press Enter to skip):")
    groq_key = input("GROQ_API_KEY: ").strip() or "your-groq-key-here"
    telegram_token = input("TELEGRAM_BOT_TOKEN: ").strip() or "your-telegram-token-here"
    
    # Create .env content
    env_content = f"""FIREBASE_PROJECT_ID={project_id}
FIREBASE_CLIENT_EMAIL={client_email}
FIREBASE_PRIVATE_KEY="{private_key}"
GROQ_API_KEY={groq_key}
TELEGRAM_BOT_TOKEN={telegram_token}
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n" + "=" * 60)
    print("✅ .env file created successfully!")
    print("=" * 60)
    print("\nThe file has been saved as: .env")
    print("\nYou can now restart your server:")
    print("python -m uvicorn api.index:app --reload")
    

def manual_input():
    print("\n--- Manual Input Mode ---")
    print("Please enter your Firebase credentials:")
    
    project_id = input("FIREBASE_PROJECT_ID: ").strip()
    client_email = input("FIREBASE_CLIENT_EMAIL: ").strip()
    
    print("\nFor FIREBASE_PRIVATE_KEY, paste the ENTIRE private key")
    print("(including -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY-----)")
    print("Then press Enter twice when done:")
    
    private_key_lines = []
    while True:
        line = input()
        if line == "" and private_key_lines:
            break
        private_key_lines.append(line)
    
    # Join with \n and ensure proper format
    private_key = "\\n".join(private_key_lines)
    
    print("\nOptional credentials (press Enter to skip):")
    groq_key = input("GROQ_API_KEY: ").strip() or "your-groq-key-here"
    telegram_token = input("TELEGRAM_BOT_TOKEN: ").strip() or "your-telegram-token-here"
    
    # Create .env content
    env_content = f"""FIREBASE_PROJECT_ID={project_id}
FIREBASE_CLIENT_EMAIL={client_email}
FIREBASE_PRIVATE_KEY="{private_key}"
GROQ_API_KEY={groq_key}
TELEGRAM_BOT_TOKEN={telegram_token}
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n" + "=" * 60)
    print("✅ .env file created successfully!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
