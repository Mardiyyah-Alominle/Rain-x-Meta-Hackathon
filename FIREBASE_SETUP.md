# 🔐 Firebase Setup Guide

## Step 1: Get Firebase Credentials

1. **Go to Firebase Console**: https://console.firebase.google.com/
2. **Select your project** (or create a new one)
3. **Navigate to**: Project Settings (⚙️ icon) → **Service Accounts** tab
4. **Click**: "Generate New Private Key" button
5. **Download** the JSON file

## Step 2: Extract Values from JSON

The downloaded JSON file will look like this:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "...",
  "token_uri": "...",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
```

## Step 3: Create .env File

Create a file named `.env` in the project root:

```bash
c:\Users\dell-pc\Desktop\codes\Rain-x-Meta-Hackathon\.env
```

## Step 4: Add Firebase Variables

Copy these values from the JSON file to your `.env`:

```env
# From the JSON file:
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour\nPrivate\nKey\nHere\n-----END PRIVATE KEY-----\n"
```

### ⚠️ Important Notes:

1. **Private Key Format**: 
   - Keep the quotes around the private key
   - Keep the `\n` characters (they represent newlines)
   - Include the full key from `-----BEGIN PRIVATE KEY-----` to `-----END PRIVATE KEY-----`

2. **Example**:
   ```env
   FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n"
   ```

## Step 5: Add Other Variables (Optional)

If you want to use the chatbot features, also add:

```env
# For AI Chatbot (get from https://console.groq.com/keys)
GROQ_API_KEY=your-groq-api-key

# For Telegram Bot (get from @BotFather on Telegram)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

## Step 6: Restart the Backend

After creating the `.env` file, restart your backend server:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
python -m uvicorn api.index:app --reload --port 8000
```

## ✅ Verification

If Firebase is configured correctly, you should see:

```
✅ Firebase Admin SDK initialized successfully.
INFO:     Application startup complete.
```

If there's an error, you'll see:

```
🔥 CRITICAL ERROR initializing Firebase: [error message]
```

## 🔒 Security

**IMPORTANT**: 
- Never commit `.env` to Git (it's already in `.gitignore`)
- Keep your Firebase credentials secure
- Don't share your private key publicly

---

## Quick Copy Template

```env
FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=""

GROQ_API_KEY=
TELEGRAM_BOT_TOKEN=
```
