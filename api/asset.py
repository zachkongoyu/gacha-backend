"""Vercel serverless function entrypoint for asset service."""
from services.asset.main import app

# Export app as handler for Vercel
handler = app
