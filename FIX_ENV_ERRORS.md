# 🔧 Fixing .env File Parsing Errors

## The Problem

You're seeing this error:
```
python-dotenv could not parse statement starting at line 13
python-dotenv could not parse statement starting at line 14
```

This means the `.env` file has formatting issues, likely with the `FIREBASE_PRIVATE_KEY`.

## ✅ Solution: Correct .env Format

Your `.env` file should look **EXACTLY** like this:

```env
FIREBASE_PROJECT_ID=your-project-id-here
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7...(your key here)...aBcD\n-----END PRIVATE KEY-----\n"

GROQ_API_KEY=your-groq-api-key-here
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
```

## 🚨 Common Mistakes to Avoid

### ❌ WRONG - Multi-line private key:
```env
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASC...
-----END PRIVATE KEY-----"
```

### ✅ CORRECT - Single line with \n:
```env
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC...\n-----END PRIVATE KEY-----\n"
```

## 📝 Step-by-Step Fix

### 1. Open your `.env` file
Location: `c:\Users\dell-pc\Desktop\codes\Rain-x-Meta-Hackathon\.env`

### 2. Check the FIREBASE_PRIVATE_KEY line

It should be **ONE SINGLE LINE** with `\n` characters (not actual line breaks).

### 3. If you copied from Firebase JSON:

The JSON file has the key like this:
```json
"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQI...\n-----END PRIVATE KEY-----\n"
```

**Copy it EXACTLY as shown** (including the `\n` characters).

### 4. Make sure there are NO:
- ❌ Actual line breaks inside the quotes
- ❌ Extra spaces
- ❌ Missing quotes at the start or end
- ❌ Comments on the same line

### 5. Example of a CORRECT .env file:

```env
FIREBASE_PROJECT_ID=my-ecommerce-bot
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-abc123@my-ecommerce-bot.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7RjHR...(very long string)...aBcDeFg==\n-----END PRIVATE KEY-----\n"

GROQ_API_KEY=gsk_abc123xyz
TELEGRAM_BOT_TOKEN=123456:ABC-DEF
```

## 🧪 Quick Test

After fixing, save the file and the server should auto-reload. You should see:

```
✅ Firebase Admin SDK initialized successfully.
INFO:     Application startup complete.
```

## 🆘 Still Having Issues?

### Option 1: Use a Simple Test Value

To test if the format is correct, temporarily use this:

```env
FIREBASE_PROJECT_ID=test-project
FIREBASE_CLIENT_EMAIL=test@test.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\ntest-key-content\n-----END PRIVATE KEY-----\n"
GROQ_API_KEY=test-key
TELEGRAM_BOT_TOKEN=test-token
```

If the server starts without parsing errors, the format is correct. Then replace with your real values.

### Option 2: Check for Hidden Characters

- Make sure you're using a plain text editor (Notepad, VS Code, etc.)
- Don't use Word or rich text editors
- Check there are no invisible characters

## 📋 Checklist

- [ ] Private key is on ONE line
- [ ] Private key has `\n` characters (not actual line breaks)
- [ ] Private key is wrapped in double quotes
- [ ] No comments on the same line as values
- [ ] No extra spaces before or after `=`
- [ ] File is saved as `.env` (not `.env.txt`)
