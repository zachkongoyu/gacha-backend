"""Vercel serverless function entrypoint for AI service."""

from services.ai.main import app

# Export app as handler for Vercel
handler = app
