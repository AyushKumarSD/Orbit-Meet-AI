# Force Vercel to Use requirements.txt Instead of pyproject.toml

## Problem
Vercel is detecting both `pyproject.toml` and `requirements.txt` and choosing `pyproject.toml`, which includes all large dependencies.

## Solution

I've updated the root `requirements.txt` to match the minimal `api/requirements.txt`. However, Vercel might still prefer `pyproject.toml`.

### Option 1: Temporarily Rename pyproject.toml (Recommended)

Add this to your Vercel project settings:

**In Vercel Dashboard → Project Settings → Build & Development Settings:**

1. **Install Command**: 
   ```bash
   mv pyproject.toml pyproject.toml.backup && pip install -r requirements.txt
   ```

2. **Build Command**: Leave as default (or your frontend build command)

### Option 2: Use Build Script

Create a `build.sh` script and configure Vercel to run it:

```bash
#!/bin/bash
# Rename pyproject.toml temporarily
mv pyproject.toml pyproject.toml.backup 2>/dev/null || true
# Continue with normal build
```

Then in Vercel settings, set build command to: `bash build.sh && vercel build`

### Option 3: Remove pyproject.toml from Git (Not Recommended)

If `pyproject.toml` is only for local development:
1. Add `pyproject.toml` to `.gitignore`
2. Keep `requirements.txt` in Git
3. Vercel will only see `requirements.txt`

**Note**: This might break local development if you use `uv`.

### Option 4: Use Vercel Environment Variable

Set in Vercel Dashboard → Environment Variables:
- `PIP_REQUIRE_VIRTUALENV=false`
- `PIP_USE_PEP517=false`

This might force pip to use requirements.txt.

## Current Status

✅ Root `requirements.txt` updated to minimal dependencies
✅ `api/requirements.txt` has minimal dependencies  
⚠️ Vercel still detecting `pyproject.toml` first

## Quick Fix (Try This First)

1. Go to Vercel Dashboard
2. Project Settings → Build & Development Settings
3. Under "Install Command", add:
   ```bash
   pip install -r requirements.txt
   ```
4. Save and redeploy

This should force Vercel to use `requirements.txt` instead of `pyproject.toml`.

