"""Vercel serverless function entrypoint for inventory service."""
from services.inventory.main import app

# Export app as handler for Vercel
handler = app
