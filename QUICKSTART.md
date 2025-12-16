# 🚀 Quick Start Guide

## Running the AestheticBot Admin Dashboard

### Step 1: Start the Backend (FastAPI)

Open a **new terminal** and run:

```bash
cd c:/Users/dell-pc/Desktop/codes/Rain-x-Meta-Hackathon
python -m uvicorn api.index:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**API Documentation**: http://localhost:8000/docs

---

### Step 2: Start the Frontend (Next.js)

Open **another terminal** and run:

```bash
cd c:/Users/dell-pc/Desktop/codes/Rain-x-Meta-Hackathon/admin-dashboard
npm run dev
```

**Expected Output**:
```
✓ Compiled successfully
- Local: http://localhost:3000
```

**Dashboard**: http://localhost:3000

---

## ✅ Verification

1. **Backend**: Visit http://localhost:8000/docs - You should see the FastAPI Swagger UI
2. **Frontend**: Visit http://localhost:3000 - You should see the admin dashboard
3. **Test Connection**: The dashboard should load stats without errors

---

## 🐛 Troubleshooting

### "uvicorn: command not found"
**Solution**: Use `python -m uvicorn` instead of just `uvicorn`

### "Module not found" errors
**Solution**: Install dependencies:
```bash
pip install fastapi uvicorn python-dotenv firebase-admin pydantic
```

### Frontend shows "Failed to load data"
**Solution**: Make sure the backend is running on port 8000

### Google Fonts errors in Next.js
**Solution**: Already fixed! The app now uses system fonts.

---

## 📝 Environment Variables Needed

### Backend (.env file)
Create a `.env` file in the project root with:
```env
GROQ_API_KEY=your_groq_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
```

### Frontend (.env.local file)
Already created in `admin-dashboard/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🎯 What You Can Do

### Without Backend Running:
- ✅ View the dashboard UI
- ✅ Navigate between pages
- ❌ Load data or perform actions

### With Backend Running:
- ✅ Everything works!
- ✅ Add/edit/delete products
- ✅ Record manual sales
- ✅ View analytics and stats
