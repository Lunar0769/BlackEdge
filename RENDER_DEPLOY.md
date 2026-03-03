# 🚀 Deploy BlackEdge to Render.com

Complete guide to deploy BlackEdge on Render's free tier.

## Prerequisites

- GitHub account with BlackEdge repository
- Render.com account (free)
- Google Gemini API key

## Step-by-Step Deployment

### 1. Prepare Repository

All necessary files are already in the repository:
- ✅ `render.yaml` - Render configuration
- ✅ `Procfile` - Process configuration
- ✅ `runtime.txt` - Python version
- ✅ `requirements.txt` - Dependencies (with gunicorn)
- ✅ `app.py` - Updated for production

### 2. Push to GitHub

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 3. Deploy on Render

#### Option A: Using render.yaml (Recommended)

1. Go to https://render.com
2. Sign in with GitHub
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub account if not already connected
5. Select repository: **Lunar0769/BlackEdge**
6. Render will automatically detect `render.yaml`
7. Click **"Apply"**

#### Option B: Manual Setup

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repository: **Lunar0769/BlackEdge**
4. Configure:
   - **Name**: `blackedge`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan**: Free
5. Click **"Create Web Service"**

### 4. Add Environment Variables

After service is created:

1. Go to your service dashboard
2. Click **"Environment"** in left sidebar
3. Add environment variable:
   - **Key**: `GOOGLE_API_KEY`
   - **Value**: Your Gemini API key
4. Click **"Save Changes"**

Service will automatically redeploy.

### 5. Access Your App

Once deployed (takes 2-5 minutes):
- Your app will be live at: `https://blackedge.onrender.com`
- Or custom URL: `https://your-service-name.onrender.com`

## Render Configuration Details

### Service Settings

```yaml
Name: blackedge
Environment: Python 3
Region: Oregon (US West)
Plan: Free
Branch: main
```

### Build Settings

```bash
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --workers 2 --timeout 120
```

Note: Render automatically binds to $PORT, no need to specify --bind

### Environment Variables

| Key | Value | Required |
|-----|-------|----------|
| `GOOGLE_API_KEY` | Your Gemini API key | ✅ Yes |
| `PYTHON_VERSION` | 3.11.0 | Auto-set |
| `PORT` | Auto-assigned by Render | Auto-set |

## Free Tier Limitations

Render Free Tier includes:
- ✅ 750 hours/month (enough for 24/7)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Spins down after 15 min of inactivity
- ⚠️ Cold start takes ~30 seconds

### Handling Cold Starts

The app will sleep after 15 minutes of inactivity. First request after sleep takes ~30 seconds.

**Solutions:**
1. Use a service like UptimeRobot to ping every 14 minutes
2. Upgrade to paid plan ($7/month) for always-on
3. Accept the cold start delay

## Troubleshooting

### Build Fails

**Error**: `Could not find a version that satisfies the requirement`

**Fix**: Check `requirements.txt` has all dependencies:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### App Crashes on Start

**Error**: `Application failed to start`

**Fix**: Check logs in Render dashboard:
1. Go to service dashboard
2. Click "Logs" tab
3. Look for error messages

Common issues:
- Missing `GOOGLE_API_KEY` environment variable
- Port binding issue (make sure using `$PORT`)

### API Key Not Working

**Error**: `GOOGLE_API_KEY not found`

**Fix**:
1. Go to Environment tab
2. Verify `GOOGLE_API_KEY` is set
3. Click "Manual Deploy" → "Deploy latest commit"

### Memory Issues

**Error**: `Out of memory`

**Fix**: Free tier has 512MB RAM. If exceeded:
1. Reduce workers in Procfile: `--workers 1`
2. Or upgrade to paid plan

## Monitoring

### View Logs

```bash
# In Render dashboard
1. Go to your service
2. Click "Logs" tab
3. See real-time logs
```

### Check Status

```bash
# Visit your app URL
https://blackedge.onrender.com

# Should show BlackEdge interface
```

## Custom Domain (Optional)

1. Go to service dashboard
2. Click "Settings"
3. Scroll to "Custom Domain"
4. Add your domain
5. Update DNS records as instructed

## Updating Your App

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Render auto-deploys on push
```

## Commands Reference

### Local Testing Before Deploy

```bash
# Install dependencies
pip install -r requirements.txt

# Test with gunicorn locally
gunicorn app:app --bind 0.0.0.0:5000 --workers 2

# Open http://localhost:5000
```

### Force Redeploy on Render

1. Go to service dashboard
2. Click "Manual Deploy"
3. Select "Deploy latest commit"

### View Environment Variables

1. Service dashboard → "Environment"
2. See all variables
3. Add/Edit/Delete as needed

## Security Notes

- ✅ Never commit `.env` file (already in .gitignore)
- ✅ Use Render's environment variables for secrets
- ✅ HTTPS is automatic on Render
- ✅ API key is encrypted in Render

## Cost

**Free Tier**: $0/month
- 750 hours/month
- Sleeps after 15 min inactivity
- 512MB RAM
- Shared CPU

**Starter Plan**: $7/month
- Always on (no sleep)
- 512MB RAM
- Shared CPU

**Standard Plan**: $25/month
- Always on
- 2GB RAM
- Dedicated CPU

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- BlackEdge Issues: https://github.com/Lunar0769/BlackEdge/issues

---

## Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Connect GitHub to Render
- [ ] Create new Web Service (Blueprint or Manual)
- [ ] Add `GOOGLE_API_KEY` environment variable
- [ ] Wait for deployment (2-5 minutes)
- [ ] Visit your app URL
- [ ] Test with a market query

**Your BlackEdge app will be live!** 🔥

---

**Deployment URL**: https://blackedge.onrender.com (or your custom URL)
