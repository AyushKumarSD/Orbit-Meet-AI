# Fixing Vercel 404 Error

## Problem
Getting `404: NOT_FOUND` error on Vercel frontend deployment.

## Solution Applied

### Updated vercel.json
Changed from using `builds` configuration to using direct build commands. This ensures:
1. Build command runs from the correct directory (`src/frontend`)
2. Output directory is correctly specified
3. Routes point to the correct location

## What Changed

**Before** (using builds):
- Used `@vercel/static-build` with builds config
- Routes pointed to `src/frontend/dist/$1`

**After** (direct configuration):
- Build command: `cd src/frontend && npm install && npm run build`
- Output directory: `src/frontend/dist`
- Routes point to root (`/$1` and `/index.html`)

## Next Steps

1. **Commit and push**:
   ```bash
   git add vercel.json
   git commit -m "Fix Vercel 404 - update build configuration"
   git push
   ```

2. **Vercel will auto-redeploy**

3. **Verify**:
   - Visit your Vercel URL
   - Should load the React app
   - Check browser console for any errors

## Additional Configuration

### Set Environment Variable in Vercel

Make sure you've set the backend URL:

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Add: `VITE_API_URL` = `https://your-backend.onrender.com`
   (Replace with your actual Render backend URL)
3. **Redeploy** after adding the variable

## Troubleshooting

### Still Getting 404?

1. **Check Build Logs**:
   - Vercel Dashboard → Deployments → Click on deployment
   - Look for build errors

2. **Verify Build Output**:
   - Check if `src/frontend/dist` exists after build
   - Verify `index.html` is in the dist folder

3. **Check Routes**:
   - Try accessing: `https://your-app.vercel.app/index.html`
   - If that works, routing is the issue

4. **Clear Cache**:
   - Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
   - Or test in incognito mode

### Build Fails?

1. **Check Node Version**:
   - Vercel should auto-detect, but you can set it in settings
   - Should be Node 18+

2. **Check Dependencies**:
   - Verify `src/frontend/package.json` has all dependencies
   - Check build logs for missing packages

3. **Check Build Command**:
   - Should be: `cd src/frontend && npm install && npm run build`
   - Verify this works locally

## Expected Result

After fixing:
- ✅ Frontend loads at root URL
- ✅ No 404 errors
- ✅ React app renders correctly
- ✅ API calls go to Render backend (if `VITE_API_URL` is set)

---

**The 404 should now be fixed!** 🎉

