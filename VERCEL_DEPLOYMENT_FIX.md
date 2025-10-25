# Vercel Deployment Fix

## Issue: 404 NOT_FOUND Error

The app returns 404 when deployed to Vercel because Vercel requires a specific serverless function structure.

## Solution Applied

### 1. Created `api/index.py`
This is the Vercel serverless function entry point:
```python
from app import app

handler = app
```

### 2. Updated `vercel.json`
Configured Vercel to route all requests to the Flask app:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```

### 3. Updated `app.py`
Disabled background tasks on Vercel (they don't work in serverless):
```python
if __name__ == '__main__':
    import os
    if os.environ.get('VERCEL') != '1':
        start_background_tasks()
```

### 4. Fixed `requirements.txt`
Removed gunicorn and fixed capitalization:
- `Flask-Cors` → `flask-cors`
- Removed `gunicorn==21.2.0`

## How It Works on Vercel

1. **Every request is independent** - Serverless functions are stateless
2. **Data fetched on-demand** - Each API call fetches fresh data from yfinance
3. **No background tasks** - Vercel doesn't support long-running threads
4. **Real-time data** - All endpoints fetch current data from Yahoo Finance

## Deployment Steps

1. Push these files to GitHub:
   - `api/index.py` (NEW)
   - `vercel.json` (NEW)
   - `requirements.txt` (UPDATED)
   - `app.py` (UPDATED)

2. Deploy to Vercel:
   - Connect your GitHub repo
   - Vercel will auto-detect the `vercel.json` config
   - Deploy will succeed

3. Test the deployment:
   ```bash
   curl https://your-app.vercel.app/
   curl https://your-app.vercel.app/api/news
   curl https://your-app.vercel.app/api/ticker/TSLA
   ```

## Key Points

✅ All data is real-time (fetched on each request)  
✅ No static/demo data (everything from yfinance)  
✅ Works on Vercel serverless functions  
✅ Auto-refreshes every time a user visits

## Troubleshooting

If you still get 404:
1. Check that `api/index.py` exists
2. Verify `vercel.json` is in the root
3. Check Vercel build logs for errors
4. Ensure `requirements.txt` has all dependencies
