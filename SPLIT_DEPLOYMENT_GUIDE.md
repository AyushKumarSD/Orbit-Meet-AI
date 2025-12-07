# Split Deployment Guide: Vercel (Frontend) + Render (Backend)

This guide covers deploying OrbitMeetAI with frontend on Vercel and backend on Render.

## 🏗️ Architecture

```
┌─────────────────┐
│   Vercel        │
│   (Frontend)    │  ────┐
│   React App     │      │
└─────────────────┘      │
                         │ HTTP Requests
                         │
┌─────────────────┐      │
│   Render        │  ◄───┘
│   (Backend)     │
│   FastAPI       │
└─────────────────┘
```

## 📋 Quick Setup Checklist

### Backend (Render)
- [ ] Sign up at render.com
- [ ] Create Web Service
- [ ] Connect GitHub repository
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variables (GROQ_API_KEY, MONGO_URI, VOYAGE_API_KEY)
- [ ] Deploy and get backend URL

### Frontend (Vercel)
- [ ] Deploy frontend to Vercel (already configured)
- [ ] Add environment variable: `VITE_API_URL=https://your-backend.onrender.com`
- [ ] Redeploy frontend

## 🚀 Step-by-Step

### Part 1: Deploy Backend to Render

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**:
   ```
   Name: orbitmeetai-backend
   Region: (choose closest to users)
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**:
   - `GROQ_API_KEY` = your_groq_key
   - `MONGO_URI` = your_mongodb_uri
   - `VOYAGE_API_KEY` = your_voyage_key
   - (Optional) `SMTP_EMAIL`, `SMTP_PASSWORD`, etc.

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your backend URL (e.g., `https://orbitmeetai-backend.onrender.com`)

### Part 2: Configure Frontend on Vercel

1. **Go to Vercel Dashboard**: [vercel.com/dashboard](https://vercel.com/dashboard)

2. **Add Environment Variable**:
   - Go to your project → Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend.onrender.com`
   - (Replace with your actual Render backend URL)
   - Select: Production, Preview, Development

3. **Redeploy**:
   - Go to Deployments tab
   - Click "..." → "Redeploy"
   - Or push a new commit

### Part 3: Test

1. **Backend Health**: 
   ```
   https://your-backend.onrender.com/health
   ```
   Should return: `{"status":"ok","message":"Service is healthy"}`

2. **Frontend**: 
   ```
   https://your-frontend.vercel.app
   ```
   Should load and connect to backend

3. **API from Frontend**: 
   - Open browser DevTools → Network tab
   - Check API requests go to Render backend URL

## 🔧 Configuration Files

### render.yaml
Already created in your project. Contains Render service configuration.

### vercel.json
Updated to only build frontend (backend removed).

### Frontend API Config
Updated to use `VITE_API_URL` environment variable.

## ⚠️ Important Notes

### Free Tier Limitations

**Render Free Tier**:
- Sleeps after 15 minutes of inactivity
- Cold start takes 30-60 seconds
- **Solution**: Use [UptimeRobot](https://uptimerobot.com) (free) to ping every 5 minutes

**Vercel Free Tier**:
- Unlimited deployments
- No sleep
- Perfect for frontend

### CORS

Backend already allows all origins. For production, you can restrict:

```python
# In src/backend/main.py
allow_origins=[
    "https://your-frontend.vercel.app",
    "https://*.vercel.app",
]
```

### Environment Variables

**Render (Backend)**:
- `GROQ_API_KEY`
- `MONGO_URI`
- `VOYAGE_API_KEY`
- (Optional) SMTP settings

**Vercel (Frontend)**:
- `VITE_API_URL` = `https://your-backend.onrender.com`

## 🔄 Updating

### Backend Updates
1. Push code to GitHub
2. Render auto-deploys
3. Wait 5-10 minutes

### Frontend Updates
1. Push code to GitHub
2. Vercel auto-deploys
3. Usually completes in 1-2 minutes

## 🐛 Troubleshooting

### Frontend Can't Connect to Backend

1. **Check Environment Variable**:
   - Vercel Dashboard → Environment Variables
   - Verify `VITE_API_URL` is set correctly

2. **Check Backend URL**:
   - Test backend directly: `https://your-backend.onrender.com/health`
   - If it works, backend is fine

3. **Check CORS**:
   - Backend should allow your Vercel domain
   - Check browser console for CORS errors

### Backend Not Starting

1. **Check Logs**:
   - Render Dashboard → Logs tab
   - Look for errors

2. **Common Issues**:
   - Missing environment variables
   - Wrong start command
   - Port not using `$PORT`

### Slow Response Times

- **First Request**: Normal if service was sleeping (30-60s)
- **Subsequent Requests**: Should be fast
- **Solution**: Keep service awake with UptimeRobot

## 📊 Monitoring

### Render
- Dashboard → Your Service → Metrics
- View CPU, Memory, Requests

### Vercel
- Dashboard → Your Project → Analytics
- View page views, performance

## 💰 Cost Summary

| Service | Cost | Notes |
|---------|------|-------|
| Vercel (Frontend) | **Free** | Unlimited deployments |
| Render (Backend) | **Free** | 750 hours/month, sleeps after 15min |
| UptimeRobot | **Free** | Keep backend awake |

**Total: $0/month** (if you keep backend awake with UptimeRobot)

## ✅ Success Checklist

- [ ] Backend deployed on Render
- [ ] Backend URL obtained
- [ ] `VITE_API_URL` set in Vercel
- [ ] Frontend redeployed on Vercel
- [ ] Backend health check works
- [ ] Frontend loads correctly
- [ ] API calls work from frontend
- [ ] UptimeRobot configured (optional, to keep backend awake)

---

**You're all set!** Your app is now deployed with frontend on Vercel and backend on Render. 🎉

