# Vercel Python serverless function
from app import app

# Export the app as 'handler' for Vercel
# Background tasks will not run in serverless environment
# Data will be fetched on-demand for each API call

handler = app
