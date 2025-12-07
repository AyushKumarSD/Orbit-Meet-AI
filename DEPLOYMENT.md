# Deploying OrbitMeetAI on Vercel

This guide will walk you through deploying OrbitMeetAI on Vercel, including both the frontend and backend.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional, for local testing):
   ```bash
   npm i -g vercel
   ```
3. **GitHub/GitLab/Bitbucket Repository**: Your code should be in a Git repository

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

Ensure all files are committed and pushed to your Git repository:

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Install Vercel CLI (Optional)

If you want to test locally or deploy via CLI:

```bash
npm install -g vercel
```

### Step 3: Configure Environment Variables

Before deploying, you'll need to set up environment variables in Vercel:

#### Required Environment Variables:

1. **GROQ_API_KEY**: Your Groq API key
2. **MONGO_URI**: Your MongoDB connection string
3. **VOYAGE_API_KEY**: Your Voyage AI API key

#### Optional Environment Variables:

- **SMTP_EMAIL**: Email for notifications
- **SMTP_PASSWORD**: Email password
- **SMTP_SERVER**: SMTP server (default: smtp.gmail.com)
- **SMTP_PORT**: SMTP port (default: 465)
- **PARTICIPANT_DB_PATH**: Path to participants database CSV

### Step 4: Deploy via Vercel Dashboard

1. **Go to Vercel Dashboard**: [vercel.com/dashboard](https://vercel.com/dashboard)
2. **Click "Add New Project"**
3. **Import your Git repository**
4. **Configure Project Settings**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (project root)
   - **Build Command**: `cd src/frontend && npm install && npm run build`
   - **Output Directory**: `src/frontend/dist`
   
   **Note**: 
   - **Frontend**: Will be BUILT (compiled to static files) - you don't need to run it
   - **Backend**: Will be automatically packaged as serverless functions - you don't need to run it
   - Vercel handles everything automatically based on `vercel.json`
   
5. **Add Environment Variables**:
   - Click "Environment Variables"
   - Add all required variables (see Step 3)
   - Make sure to add them for Production, Preview, and Development
6. **Click "Deploy"**

### Step 5: Deploy via CLI (Alternative)

If you prefer using the CLI:

```bash
# Login to Vercel
vercel login

# Deploy (first time)
vercel

# Deploy to production
vercel --prod
```

During the first deployment, Vercel will ask:
- **Set up and deploy?** → Yes
- **Which scope?** → Your account/team
- **Link to existing project?** → No (for first deployment)
- **Project name?** → orbitmeetai (or your preferred name)
- **Directory?** → `./` (current directory)

### Step 6: Configure Environment Variables in Vercel

After deployment, add environment variables:

**Via Dashboard:**
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add each variable for Production, Preview, and Development

**Via CLI:**
```bash
vercel env add GROQ_API_KEY
vercel env add MONGO_URI
vercel env add VOYAGE_API_KEY
# ... add other variables as needed
```

## 📁 Project Structure for Vercel

The deployment uses the following structure:

```
OrbitMeetAI/
├── api/
│   └── index.py              # Vercel serverless function handler
├── src/
│   ├── backend/
│   │   └── main.py           # FastAPI app
│   └── frontend/
│       └── dist/             # Built frontend (generated)
├── vercel.json               # Vercel configuration
└── .vercelignore            # Files to ignore
```

## ⚙️ How It Works

### Backend (API Routes)

- All API requests to `/api/*` are routed to `api/index.py`
- The handler uses `Mangum` to convert FastAPI to ASGI for Vercel serverless functions
- Each API endpoint becomes a serverless function

### Frontend

- Built using Vite during deployment
- Static files served from `src/frontend/dist`
- API calls are proxied to `/api/*` routes

## ⚠️ Important Limitations & Considerations

### 1. Background Scheduler

**The background scheduler will NOT work on Vercel** because:
- Vercel serverless functions are stateless and short-lived
- Background processes don't persist between function invocations
- APScheduler requires a persistent process

**Solutions:**

#### Option A: Use Vercel Cron Jobs (Recommended)
Create `vercel.json` cron configuration:

```json
{
  "crons": [{
    "path": "/api/trigger-scheduler",
    "schedule": "0 * * * *"
  }]
}
```

Then modify the endpoint to work without the scheduler:

```python
# In src/backend/main.py, modify /trigger-scheduler endpoint
# to directly call process_unprocessed_meetings()
```

#### Option B: Use External Cron Service
- Use services like [cron-job.org](https://cron-job.org) or [EasyCron](https://www.easycron.com)
- Set up a cron job to call `https://your-app.vercel.app/api/trigger-scheduler` every hour

#### Option C: Deploy Backend Separately
- Deploy backend to Railway, Render, or Fly.io for persistent processes
- Keep frontend on Vercel
- Update frontend API URL to point to backend URL

### 2. Function Timeout

- Vercel Pro: 60 seconds timeout
- Vercel Hobby: 10 seconds timeout

**For long-running operations** (like processing meetings):
- Consider using background jobs
- Or deploy backend separately (see Option C above)

### 3. Cold Starts

- First request after inactivity may be slow (cold start)
- Consider using Vercel Pro for better performance
- Or keep functions warm with a ping service

### 4. File System

- Vercel serverless functions have read-only filesystem
- Don't rely on local file storage
- Use MongoDB or cloud storage for all data

## 🔧 Post-Deployment Configuration

### 1. Update CORS Settings

In `src/backend/main.py`, update CORS to allow your Vercel domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",
        "https://*.vercel.app",  # For preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Update Frontend API URL

The frontend should automatically use `/api` in production. Verify in `src/frontend/src/services/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.DEV ? '/api' : '/api');
```

### 3. Test Your Deployment

1. Visit your Vercel deployment URL
2. Check API health: `https://your-app.vercel.app/api/health`
3. Test API docs: `https://your-app.vercel.app/api/docs`

## 🔄 Updating Your Deployment

### Via Dashboard:
1. Push changes to your Git repository
2. Vercel automatically detects and deploys

### Via CLI:
```bash
vercel --prod
```

## 🐛 Troubleshooting

### Build Fails

**Error: Module not found**
- Ensure all dependencies are in `pyproject.toml`
- Check that `mangum` is installed

**Error: Frontend build fails**
- Check Node.js version (should be 18+)
- Verify `src/frontend/package.json` has correct build script

### API Returns 500 Errors

**Check Vercel Function Logs:**
1. Go to Vercel Dashboard
2. Navigate to your project
3. Click "Functions" tab
4. View logs for errors

**Common Issues:**
- Missing environment variables
- MongoDB connection issues
- API key errors

### CORS Errors

- Update CORS settings in `src/backend/main.py`
- Ensure frontend URL is in `allow_origins`

### Function Timeout

- Long-running operations may timeout
- Consider splitting into smaller functions
- Or use background job processing

## 📊 Monitoring

### Vercel Analytics

Enable Vercel Analytics in project settings to monitor:
- Function execution times
- Error rates
- Request volumes

### Logs

View real-time logs:
- Dashboard → Project → Functions → Logs
- Or use Vercel CLI: `vercel logs`

## 🔐 Security Best Practices

1. **Never commit `.env` files**
2. **Use Vercel Environment Variables** for all secrets
3. **Enable Vercel Authentication** if needed
4. **Use HTTPS** (automatic on Vercel)
5. **Restrict CORS** to your domains only
6. **Rotate API keys** regularly

## 💰 Cost Considerations

- **Vercel Hobby**: Free tier with limitations
- **Vercel Pro**: $20/month for better performance
- **Function Execution**: Monitor usage to avoid overages

## 🚀 Alternative Deployment Options

If Vercel doesn't meet your needs:

1. **Backend**: Railway, Render, Fly.io, or AWS Lambda
2. **Frontend**: Vercel, Netlify, or Cloudflare Pages
3. **Full Stack**: Railway or Render (both frontend + backend)

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Mangum Documentation](https://mangum.io/)
- [FastAPI on Vercel](https://vercel.com/guides/deploying-fastapi-with-vercel)

---

**Need Help?** Check Vercel's [support documentation](https://vercel.com/support) or open an issue in your repository.

