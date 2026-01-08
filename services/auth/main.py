"""Auth service main application with OAuth callback."""
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx

from shared.settings import settings
from shared.auth import create_access_token
from shared.database import create_db_pool, close_db_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan (startup and shutdown)."""
    # Startup
    await create_db_pool()
    yield
    # Shutdown
    await close_db_pool()


app = FastAPI(
    title="Auth Service",
    description="Authentication service with OAuth support",
    version="0.1.0",
    lifespan=lifespan
)


class TokenResponse(BaseModel):
    """OAuth token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    user_info: Optional[dict] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": "auth", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/auth/login")
async def login():
    """
    Initiate OAuth login flow.
    Redirects to OAuth provider's authorization page.
    """
    if not settings.oauth_client_id:
        raise HTTPException(status_code=500, detail="OAuth not configured")
    
    # Build authorization URL
    auth_url = (
        f"{settings.oauth_authorize_url}"
        f"?client_id={settings.oauth_client_id}"
        f"&redirect_uri={settings.oauth_redirect_uri}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    
    return {
        "auth_url": auth_url,
        "message": "Redirect user to auth_url to begin OAuth flow"
    }


@app.get("/auth/callback", response_model=TokenResponse)
async def oauth_callback(code: str = Query(..., description="OAuth authorization code")):
    """
    OAuth callback endpoint.
    Exchanges authorization code for access token and fetches user info.
    Issues JWT token for authenticated user.
    
    Args:
        code: Authorization code from OAuth provider
        
    Returns:
        JWT access token and user information
    """
    if not settings.oauth_client_id or not settings.oauth_client_secret:
        raise HTTPException(status_code=500, detail="OAuth not configured")
    
    async with httpx.AsyncClient() as client:
        # Exchange authorization code for access token
        token_data = {
            "code": code,
            "client_id": settings.oauth_client_id,
            "client_secret": settings.oauth_client_secret,
            "redirect_uri": settings.oauth_redirect_uri,
            "grant_type": "authorization_code",
        }
        
        try:
            token_response = await client.post(
                settings.oauth_token_url,
                data=token_data,
                timeout=10.0
            )
            token_response.raise_for_status()
            tokens = token_response.json()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to exchange code for token: {str(e)}"
            )
        
        # Fetch user information
        oauth_access_token = tokens.get("access_token")
        if not oauth_access_token:
            raise HTTPException(status_code=400, detail="No access token received")
        
        try:
            userinfo_response = await client.get(
                settings.oauth_userinfo_url,
                headers={"Authorization": f"Bearer {oauth_access_token}"},
                timeout=10.0
            )
            userinfo_response.raise_for_status()
            user_info = userinfo_response.json()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch user info: {str(e)}"
            )
    
    # Extract user details
    user_id = user_info.get("id") or user_info.get("sub", "unknown")
    email = user_info.get("email")
    
    # Create JWT token for our application
    jwt_token = create_access_token(
        data={
            "sub": user_id,
            "email": email,
        }
    )
    
    return TokenResponse(
        access_token=jwt_token,
        token_type="bearer",
        expires_in=settings.jwt_access_token_expire_minutes * 60,
        user_info=user_info
    )


@app.post("/auth/verify")
async def verify_token(token: str):
    """
    Verify a JWT token.
    
    Args:
        token: JWT token to verify
        
    Returns:
        Token validity status
    """
    from shared.auth import decode_access_token
    
    token_data = decode_access_token(token)
    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {
        "valid": True,
        "user_id": token_data.user_id,
        "email": token_data.email
    }
