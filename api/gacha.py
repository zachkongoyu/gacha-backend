"""Vercel serverless function entrypoint for gacha service."""

from services.gacha.main import app

# Export app as handler for Vercel
handler = app
