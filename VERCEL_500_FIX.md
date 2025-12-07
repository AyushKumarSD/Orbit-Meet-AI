# Fixing Vercel 500 Error: Serverless Function Crashed

## Problem
Vercel is trying to deploy the `api/` directory as a serverless function, causing a 500 error. This happens because:
- Vercel automatically detects `api/` directories and tries to deploy them
- The backend is now on Render, not Vercel
- The serverless function fails because it's not configured for Vercel

## Solution Applied

### Added `api/` to `.vercelignore`
This prevents Vercel from detecting and trying to deploy the `api/` directory as serverless functions.

## What Changed

**`.vercelignore`** now includes:
```
api/
```

This tells Vercel to ignore the `api/` directory completely during deployment.

## Next Steps

1. **Commit and push**:
   ```bash
   git add .vercelignore
   git commit -m "Ignore api directory - backend on Render"
   git push
   ```

2. **Vercel will auto-redeploy**

3. **Verify**:
   - Visit your Vercel URL
   - Should load frontend without 500 errors
   - Check Vercel Functions tab - should show no functions

## Important: Set Backend URL

Make sure you've configured the frontend to use your Render backend:

1. **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Add: `VITE_API_URL` = `https://your-backend.onrender.com`
   (Replace with your actual Render backend URL)
3. **Redeploy** after adding

## Verification

After fixing:
- ✅ No serverless functions in Vercel
- ✅ Frontend loads correctly
- ✅ API calls go to Render backend
- ✅ No 500 errors

## Why This Happened

Vercel has automatic detection for:
- `api/` directory → Serverless Functions
- `functions/` directory → Serverless Functions

Even if not in `vercel.json`, Vercel will try to deploy these. Since we're using Render for backend, we need to explicitly ignore the `api/` directory.

---

**The 500 error should now be fixed!** 🎉

