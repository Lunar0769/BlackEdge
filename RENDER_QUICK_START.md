# ⚡ Render Quick Deploy - BlackEdge

## 🚀 Deploy in 5 Minutes

### Step 1: Go to Render
Visit: https://render.com

### Step 2: Sign In
- Click "Get Started"
- Sign in with GitHub

### Step 3: Create Web Service
1. Click **"New +"** → **"Blueprint"**
2. Select repository: **Lunar0769/BlackEdge**
3. Click **"Apply"**

### Step 4: Add API Key
1. After service is created, go to **"Environment"**
2. Add variable:
   - Key: `GOOGLE_API_KEY`
   - Value: `your_gemini_api_key_here`
3. Click **"Save Changes"**

### Step 5: Wait for Deploy
- Takes 2-5 minutes
- Watch the logs for progress

### Step 6: Access Your App
Your app will be live at:
```
https://blackedge.onrender.com
```

---

## 📋 Settings Summary

### Service Configuration
```
Name: blackedge
Environment: Python 3
Region: Oregon (US West)
Branch: main
Plan: Free
```

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Environment Variables
| Variable | Value |
|----------|-------|
| `GOOGLE_API_KEY` | Your Gemini API key |

---

## 🔧 Manual Setup (Alternative)

If Blueprint doesn't work:

1. **New Web Service**
   - Click "New +" → "Web Service"
   - Connect: Lunar0769/BlackEdge

2. **Configure**
   ```
   Name: blackedge
   Region: Oregon
   Branch: main
   Runtime: Python 3
   Build: pip install -r requirements.txt
   Start: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   Plan: Free
   ```

3. **Environment**
   - Add `GOOGLE_API_KEY`

4. **Deploy**
   - Click "Create Web Service"

---

## ⚠️ Important Notes

### Free Tier Limits
- ✅ 750 hours/month (24/7 coverage)
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Cold start: ~30 seconds

### Cold Start Solution
Use UptimeRobot (free) to ping every 14 minutes:
1. Sign up at https://uptimerobot.com
2. Add monitor: `https://blackedge.onrender.com`
3. Interval: 14 minutes

---

## 🐛 Troubleshooting

### Build Failed
- Check logs in Render dashboard
- Verify all files pushed to GitHub
- Check `requirements.txt` is complete

### App Won't Start
- Verify `GOOGLE_API_KEY` is set in Environment
- Check logs for error messages
- Try "Manual Deploy" → "Deploy latest commit"

### 404 Error
- Wait 2-5 minutes for initial deploy
- Check service status is "Live"
- Verify URL is correct

---

## 📱 Test Your Deployment

1. Visit: `https://blackedge.onrender.com`
2. Enter query: "Should I buy NVDA?"
3. Click "Analyse"
4. Watch agents work in real-time

---

## 🔄 Update Your App

```bash
# Make changes locally
git add .
git commit -m "Update"
git push

# Render auto-deploys
```

---

## 💰 Upgrade Options

**Free**: $0/month
- Sleeps after 15 min
- 512MB RAM

**Starter**: $7/month
- Always on
- 512MB RAM

**Standard**: $25/month
- Always on
- 2GB RAM

---

## 📞 Support

- Full Guide: See `RENDER_DEPLOY.md`
- Render Docs: https://render.com/docs
- Issues: https://github.com/Lunar0769/BlackEdge/issues

---

**That's it! Your BlackEdge is now live!** 🔥
