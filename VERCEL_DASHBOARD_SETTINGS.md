# Vercel Dashboard Settings

## ⚠️ Important Note

Since you have `builds` configured in `vercel.json`, Vercel will use that configuration. However, you can still set these in the dashboard as overrides.

## Recommended Settings

### Install Command
**Leave empty** or set to:
```
cd src/frontend && npm install
```

**Note**: Python dependencies are installed automatically by Vercel from `requirements.txt` (since `pyproject.toml` is ignored).

### Build Command
**Leave empty** or set to:
```
cd src/frontend && npm run build
```

**Note**: Vercel will automatically run `npm run vercel-build` from `src/frontend/package.json` which runs `npm run build`.

### Output Directory
```
src/frontend/dist
```

**Note**: This is where Vite builds your frontend.

### Development Command
```
cd src/frontend && npm run dev
```

**Note**: This is only for local development with `vercel dev`.

## Alternative: If You Remove `builds` from vercel.json

If you want to use dashboard settings instead of `vercel.json` builds:

### Install Command
```
cd src/frontend && npm install
```

### Build Command
```
cd src/frontend && npm run build
```

### Output Directory
```
src/frontend/dist
```

### Development Command
```
cd src/frontend && npm run dev
```

## Recommended Configuration (Current Setup)

Since you have `vercel.json` with `builds`:

1. **Install Command**: Leave **empty** (Vercel handles it via builds config)
2. **Build Command**: Leave **empty** (Vercel handles it via builds config)
3. **Output Directory**: Leave **empty** (specified in vercel.json)
4. **Development Command**: `cd src/frontend && npm run dev` (optional, for local dev)

## Python Dependencies

Python dependencies are automatically installed by Vercel's `@vercel/python` builder from:
- `api/requirements.txt` (if exists)
- `requirements.txt` (root level, since pyproject.toml is ignored)

**No install command needed for Python** - Vercel handles it automatically.

## Summary

**For your current setup with `vercel.json`:**

| Setting | Value | Required? |
|---------|-------|-----------|
| **Install Command** | (empty) | No - handled by builds |
| **Build Command** | (empty) | No - handled by builds |
| **Output Directory** | (empty) | No - specified in vercel.json |
| **Development Command** | `cd src/frontend && npm run dev` | Optional |

**Just leave them empty** - your `vercel.json` handles everything!

