# Deploying Backend to Render

This guide will help you deploy the OrbitMeetAI backend to Render while keeping the frontend on Vercel.

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com) (free tier available)
2. **GitHub Repository**: Your code should be in a Git repository
3. **Environment Variables**: Have your API keys ready

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

Ensure all files are committed and pushed:

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Create Web Service on Render

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `orbitmeetai-backend` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (project root)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Configure Environment Variables

In Render Dashboard → Your Service → Environment:

Add these required variables:
- `GROQ_API_KEY` - Your Groq API key
- `MONGO_URI` - Your MongoDB connection string
- `VOYAGE_API_KEY` - Your Voyage AI API key

Optional variables:
- `SMTP_EMAIL` - Email for notifications
- `SMTP_PASSWORD` - Email password
- `SMTP_SERVER` - SMTP server (default: smtp.gmail.com)
- `SMTP_PORT` - SMTP port (default: 465)
- `PARTICIPANT_DB_PATH` - Path to participants database CSV

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your FastAPI server
3. Wait for deployment to complete (usually 5-10 minutes)

### Step 5: Get Your Backend URL

After deployment, Render will provide a URL like:
```
https://orbitmeetai-backend.onrender.com
```

**Save this URL** - you'll need it for the frontend configuration.

## 🔧 Alternative: Using render.yaml

If you prefer configuration as code:

1. The `render.yaml` file is already created in your project
2. In Render Dashboard → **New +** → **"Blueprint"**
3. Connect your repository
4. Render will automatically detect and use `render.yaml`
5. Review and deploy

## 🔗 Connect Frontend to Backend

### Update Vercel Environment Variables

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Add:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```
   (Replace with your actual Render backend URL)

3. **Redeploy** your Vercel frontend

### Or Update Frontend Code

The frontend is already configured to use `VITE_API_URL` environment variable. Just set it in Vercel.

## ✅ Verify Deployment

1. **Backend Health Check**: 
   ```
   https://your-backend.onrender.com/health
   ```
   Should return: `{"status":"ok","message":"Service is healthy"}`

2. **API Documentation**: 
   ```
   https://your-backend.onrender.com/docs
   ```
   Should show FastAPI Swagger UI

3. **Frontend**: Visit your Vercel URL and test API calls

## ⚠️ Important Notes

### Free Tier Limitations

- **Sleep After Inactivity**: Free tier services sleep after 15 minutes of inactivity
- **Cold Start**: First request after sleep may take 30-60 seconds
- **Solution**: Use a ping service like [UptimeRobot](https://uptimerobot.com) to keep it awake (free)

### CORS Configuration

The backend already allows all origins (`allow_origins=["*"]`). For production, you can restrict it to your Vercel domain:

```python
# In src/backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "https://*.vercel.app",  # For preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Scheduler Works!

Unlike Vercel, Render supports persistent processes, so your background scheduler will work perfectly!

## 🔄 Updating Your Deployment

### Automatic Deployments

Render automatically deploys when you push to your connected branch.

### Manual Deploy

1. Go to Render Dashboard → Your Service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

## 🐛 Troubleshooting

### Service Won't Start

**Check Logs**:
1. Render Dashboard → Your Service → **Logs** tab
2. Look for errors in build or runtime

**Common Issues**:
- Missing environment variables
- Port not set correctly (use `$PORT`)
- Dependencies not installing

### Slow Cold Starts

- Normal for free tier (15 min sleep)
- First request after sleep is slow
- Use UptimeRobot to keep it awake

### CORS Errors

- Verify backend URL in frontend environment variable
- Check CORS settings in `src/backend/main.py`
- Ensure backend allows your Vercel domain

### Database Connection Issues

- Verify `MONGO_URI` is correct
- Check MongoDB network access (allow Render IPs)
- Test connection locally first

## 📊 Monitoring

### View Logs

Render Dashboard → Your Service → **Logs** tab

### Metrics

Render Dashboard → Your Service → **Metrics** tab
- CPU usage
- Memory usage
- Request count

## 💰 Cost

**Free Tier**:
- 750 hours/month (enough for 24/7 if you keep it awake)
- 512 MB RAM
- 0.1 CPU

**If you exceed**:
- $7/month for Starter plan
- Better performance
- No sleep

## 🎯 Next Steps

1. Deploy backend to Render
2. Get backend URL
3. Update Vercel environment variable `VITE_API_URL`
4. Redeploy frontend on Vercel
5. Test the full stack!

---

**Need Help?** Check [Render Documentation](https://render.com/docs) or open an issue in your repository.

