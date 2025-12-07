"""
Vercel serverless function handler for FastAPI backend
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variable to indicate we're on Vercel
os.environ["VERCEL"] = "1"

from mangum import Mangum
from src.backend.main import app

# Create handler for Vercel
# Using lifespan="off" because scheduler doesn't work in serverless
handler = Mangum(app, lifespan="off")

# Note: Background scheduler is disabled on Vercel
# Use Vercel Cron Jobs or external service for scheduled tasks
# See DEPLOYMENT.md for more details

