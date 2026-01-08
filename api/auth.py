"""Vercel serverless function entrypoint for auth service."""
from services.auth.main import app

# Export app as handler for Vercel
handler = app
