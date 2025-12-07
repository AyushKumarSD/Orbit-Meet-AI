# Fixing Vercel UV Workspace Error

## Problem
Vercel is trying to use `uv` and failing because of the workspace configuration in `pyproject.toml`.

## Solution Applied

1. **Commented out workspace config** in `pyproject.toml`
2. **Ensured `api/requirements.txt` exists** (Vercel will use this)
3. **Added `python3.11.9/` to `.vercelignore`** (exclude from deployment)
4. **Created `runtime.txt`** to specify Python version

## What Vercel Will Use

Vercel will automatically detect and use:
- `api/requirements.txt` for Python dependencies
- Python 3.11 (from `runtime.txt` or environment variable)

## If Error Persists

If Vercel still tries to use `uv`, you can:

### Option 1: Remove uv.lock (if exists)
```bash
# Remove uv.lock from repository
git rm uv.lock
git commit -m "Remove uv.lock for Vercel"
```

### Option 2: Force pip in Vercel Settings
In Vercel Dashboard → Project Settings → Build & Development Settings:
- Set "Install Command" to: `pip install -r api/requirements.txt`

### Option 3: Use .python-version
The `api/.python-version` file should help Vercel use the correct Python version.

## Verification

After deploying, check the build logs:
- Should see: "Installing dependencies from requirements.txt"
- Should NOT see: "uv export" or workspace-related errors

