# Fixing Vercel 250MB Serverless Function Size Limit

## Problem
Your serverless function exceeds Vercel's 250 MB unzipped size limit. This is common with Python ML/AI applications.

## Solution: Use Minimal Dependencies

I've created optimized configuration files to reduce the function size.

## ✅ What I've Done

1. **Created `requirements-vercel.txt`** - Minimal dependencies (only what's needed for API)
2. **Created `api/requirements.txt`** - Vercel will use this automatically
3. **Updated `.vercelignore`** - Excludes unnecessary files
4. **Updated `vercel.json`** - Optimized configuration

## 🚀 Quick Fix Steps

### Option 1: Use the Minimal Requirements (Recommended)

1. **Copy the minimal requirements to the api folder**:
   ```bash
   cp requirements-vercel.txt api/requirements.txt
   ```

2. **Or manually create `api/requirements.txt`** with only these packages:
   ```
   fastapi>=0.115.0
   mangum>=0.17.0
   pydantic>=2.0.0
   python-dotenv>=1.2.1
   langchain>=1.1.0
   langchain-text-splitters>=0.2.0
   langchain-groq>=1.1.0
   langchain-classic>=1.0.0
   pymongo>=4.15.4
   requests>=2.31.0
   loguru>=0.7.3
   jinja2>=3.1.6
   rapidfuzz>=3.14.3
   ```

3. **Commit and redeploy**:
   ```bash
   git add api/requirements.txt
   git commit -m "Use minimal requirements for Vercel"
   git push
   ```

### Option 2: Check Function Size

To see what's taking up space:

1. Go to Vercel Dashboard → Your Project → Functions
2. Check the function size in the logs
3. Look for large packages in the build output

## 📦 Excluded Packages (Not Needed for API)

These packages are **excluded** from the minimal requirements because:
- The API receives text directly (not files)
- They're not imported in the API code
- They add significant size

| Package | Size | Why Excluded |
|---------|------|--------------|
| `ollama` | ~100MB+ | Not used in API |
| `pdfplumber` | ~50MB+ | API receives text, not PDFs |
| `python-docx` | ~10MB | API receives text, not DOCX |
| `docx2txt` | ~5MB | API receives text, not DOCX |
| `langchain-google-genai` | ~20MB+ | Only using Groq |
| `uvicorn[standard]` | ~10MB+ | Mangum handles it |
| `apscheduler` | ~5MB | Not used on Vercel |
| `node`/`npm` | ~50MB+ | Not needed for Python |
| `numpy` | ~20MB+ | Check if actually used |

**Total Saved: ~270MB+**

## 🔍 Verify What's Actually Used

The API endpoints receive:
- `transcript: str` (text, not files)
- No file uploads
- No file processing

So file processing libraries are not needed.

## ⚠️ If You Still Exceed the Limit

### Option A: Upgrade to Vercel Pro
- Pro plan allows larger functions
- Better for ML/AI applications

### Option B: Split into Multiple Functions
- Create separate functions for different endpoints
- Each function can be smaller

### Option C: Use External Backend
- Deploy backend to Railway, Render, or Fly.io
- Keep frontend on Vercel
- Backend can be larger on these platforms

### Option D: Use Lambda Layers (Advanced)
- Move common dependencies to Lambda layers
- Reduces function size

## 📝 Testing Locally

Test with minimal requirements:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install minimal requirements
pip install -r requirements-vercel.txt

# Test API
python -m src.backend.main
```

## 🎯 Expected Size After Fix

With minimal requirements, your function should be:
- **Before**: ~300-400MB (exceeds limit)
- **After**: ~100-150MB (within limit)

## ✅ Verification Checklist

- [ ] `api/requirements.txt` exists with minimal packages
- [ ] `.vercelignore` excludes unnecessary files
- [ ] `vercel.json` is configured correctly
- [ ] Tested locally with minimal requirements
- [ ] Redeployed to Vercel
- [ ] Function size is under 250MB

## 🆘 Still Having Issues?

1. **Check build logs** in Vercel dashboard
2. **Verify** `api/requirements.txt` is being used
3. **Check** if any imports are pulling in large dependencies
4. **Consider** using `pip-tools` to pin exact versions:
   ```bash
   pip-compile requirements-vercel.txt
   ```

---

**Note**: The `api/requirements.txt` file takes precedence over root `requirements.txt` for Vercel Python functions.

