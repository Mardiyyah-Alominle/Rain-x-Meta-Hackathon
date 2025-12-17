# 🚀 Quick Deployment Checklist

Use this checklist to deploy to Vercel step-by-step.

## ✅ Pre-Deployment

- [ ] Code is working locally
- [ ] Firebase credentials are ready
- [ ] Git repository is initialized
- [ ] Code is pushed to GitHub/GitLab/Bitbucket

## 📦 Backend Deployment

- [ ] Go to https://vercel.com/dashboard
- [ ] Click "Add New" → "Project"
- [ ] Import your Git repository
- [ ] Configure:
  - Framework: Other
  - Root Directory: `./`
  - Build Command: (leave empty)
  - Output Directory: (leave empty)
- [ ] Add environment variables:
  - `FIREBASE_PROJECT_ID`
  - `FIREBASE_CLIENT_EMAIL`
  - `FIREBASE_PRIVATE_KEY` (one line with `\n`)
  - `GROQ_API_KEY`
  - `TELEGRAM_BOT_TOKEN`
- [ ] Click "Deploy"
- [ ] Copy backend URL (e.g., `https://your-project.vercel.app`)
- [ ] Test: Visit `https://your-project.vercel.app/` - should show status
- [ ] Test: Visit `https://your-project.vercel.app/docs` - should show Swagger UI

## 🎨 Frontend Deployment

- [ ] Update `admin-dashboard/.env.local`:
  ```
  NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
  ```
- [ ] Commit and push changes
- [ ] Go to Vercel Dashboard
- [ ] Click "Add New" → "Project"
- [ ] Select same repository
- [ ] Configure:
  - Framework: Next.js
  - Root Directory: `admin-dashboard`
  - Build Command: `npm run build`
  - Output Directory: `.next`
- [ ] Add environment variable:
  - `NEXT_PUBLIC_API_URL` = your backend URL
- [ ] Click "Deploy"
- [ ] Copy frontend URL
- [ ] Test: Visit dashboard URL - should load

## 🧪 Final Testing

- [ ] Dashboard loads without errors
- [ ] Can add a product
- [ ] Can record a sale
- [ ] Analytics dashboard shows data
- [ ] Check Vercel logs for any errors

## 🎉 Done!

Your app is live!
- Backend: `https://your-backend.vercel.app`
- Frontend: `https://your-dashboard.vercel.app`
