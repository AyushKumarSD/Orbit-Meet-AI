# Debugging 404 Error on Vercel

## Current Status
- ✅ Build completes successfully
- ✅ Frontend builds to `src/frontend/dist/`
- ✅ Python dependencies install from `requirements.txt`
- ❌ Still getting 404 NOT_FOUND

## Debugging Steps

### 1. Test API Endpoint Directly

Try accessing the API directly:
```
https://your-app.vercel.app/api/health
```

**If this works**: The API is fine, issue is with frontend routing.
**If this fails**: The API function has an issue.

### 2. Check Vercel Functions

1. Go to Vercel Dashboard
2. Your Project → Functions tab
3. Look for `api/index.py`
4. Check for any errors

### 3. Check Function Logs

1. Vercel Dashboard → Your Project
2. Deployments → Click on latest deployment
3. Functions → Click on `api/index.py`
4. View logs for errors

### 4. Test Root Path

Try accessing:
```
https://your-app.vercel.app/
```

**Expected**: Should serve `index.html`
**If 404**: Routing issue

### 5. Check File Structure

Verify these files exist after build:
- `src/frontend/dist/index.html`
- `src/frontend/dist/assets/` (with JS/CSS files)
- `api/index.py`

## Common Issues

### Issue 1: API Handler Not Exported

**Check**: `api/index.py` must export `handler`

```python
handler = Mangum(app, lifespan="off")
```

### Issue 2: Routes Not Matching

**Check**: Routes in `vercel.json` must match actual paths

Current routes:
- `/api/*` → `api/index.py` ✅
- Static assets → `src/frontend/dist/` ✅
- Everything else → `index.html` ✅

### Issue 3: Frontend Path Wrong

**Check**: Vite builds to `dist/` in `src/frontend/`

The path should be: `src/frontend/dist/index.html`

### Issue 4: Missing index.html

**Check**: Vite should generate `index.html` in `dist/`

If missing, check `src/frontend/index.html` exists.

## Quick Fixes to Try

### Fix 1: Simplify Routes

Try this simpler routing:

```json
{
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" },
    { "src": "/(.*)", "dest": "/src/frontend/dist/$1" }
  ]
}
```

### Fix 2: Check API Handler

Verify `api/index.py` exports handler correctly:

```python
handler = Mangum(app, lifespan="off")
```

### Fix 3: Test with curl

```bash
# Test API
curl https://your-app.vercel.app/api/health

# Test root
curl https://your-app.vercel.app/
```

## Next Steps

1. **Test API directly**: `https://your-app.vercel.app/api/health`
2. **Check Vercel Functions tab** for errors
3. **Check deployment logs** for any warnings
4. **Verify file paths** match what's in `vercel.json`

## If API Works But Frontend Doesn't

The issue is likely:
- Frontend routing configuration
- Missing `index.html` in dist
- Wrong path in `vercel.json`

## If API Also Returns 404

The issue is likely:
- API handler not exporting correctly
- Routes not matching
- Function not being created

