"""Gacha service main application with pull mechanics."""
from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import random

from shared.settings import settings
from shared.auth import decode_access_token
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
    title="Gacha Service",
    description="Gacha pull mechanics service",
    version="0.1.0",
    lifespan=lifespan
)


class PullResult(BaseModel):
    """Result from a gacha pull."""
    item_id: str
    item_name: str
    rarity: str
    is_pity: bool = False


class PullResponse(BaseModel):
    """Response from gacha pull endpoint."""
    pulls: List[PullResult]
    pity_counter: int
    next_pity_at: int


class GachaConfig(BaseModel):
    """Gacha configuration and rates."""
    total_pulls: int
    pity_counter: int
    five_star_rate: float = 0.006
    four_star_rate: float = 0.051
    pity_threshold: int = 90


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": "gacha", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """Extract user ID from JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.split(" ")[1]
    token_data = decode_access_token(token)
    
    if token_data is None:
        return None
    
    return token_data.user_id


@app.post("/pull", response_model=PullResponse)
async def pull_gacha(
    count: int = 1,
    authorization: Optional[str] = Header(None)
):
    """
    Perform gacha pulls.
    
    Args:
        count: Number of pulls to perform (1 or 10)
        authorization: JWT token in Authorization header
        
    Returns:
        Pull results with pity information
    """
    user_id = get_current_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if count not in [1, 10]:
        raise HTTPException(status_code=400, detail="Count must be 1 or 10")
    
    # Stub pity counter (in real implementation, fetch from database)
    pity_counter = 45  # Example: user is 45 pulls into pity
    pity_threshold = 90
    
    pulls = []
    current_pity = pity_counter
    
    for i in range(count):
        current_pity += 1
        is_pity = current_pity >= pity_threshold
        
        # Determine rarity based on rates or pity
        if is_pity:
            rarity = "5-star"
            current_pity = 0  # Reset pity
        else:
            # Simple probability for stub
            roll = random.random()
            if roll < 0.006:  # 0.6% for 5-star
                rarity = "5-star"
                current_pity = 0
            elif roll < 0.057:  # 5.1% for 4-star (0.006 + 0.051)
                rarity = "4-star"
            else:
                rarity = "3-star"
        
        # Generate stub item
        pulls.append(PullResult(
            item_id=f"item_{random.randint(1000, 9999)}",
            item_name=f"{rarity} Character/Weapon",
            rarity=rarity,
            is_pity=is_pity
        ))
    
    return PullResponse(
        pulls=pulls,
        pity_counter=current_pity,
        next_pity_at=pity_threshold
    )


@app.get("/rates")
async def get_rates():
    """
    Get current gacha rates and pity information.
    
    Returns:
        Gacha rates and pity thresholds
    """
    return {
        "rates": {
            "5-star": "0.6%",
            "4-star": "5.1%",
            "3-star": "94.3%"
        },
        "pity": {
            "threshold": 90,
            "guaranteed_5_star": True,
            "description": "Guaranteed 5-star at 90 pulls"
        }
    }


@app.get("/banner")
async def get_current_banner():
    """
    Get current gacha banner information.
    
    Returns:
        Current banner details
    """
    return {
        "banner_id": "banner_001",
        "name": "Featured Character Banner",
        "start_date": "2026-01-01T00:00:00Z",
        "end_date": "2026-01-31T23:59:59Z",
        "featured_items": [
            {
                "item_id": "char_001",
                "name": "Limited Character",
                "rarity": "5-star",
                "type": "character"
            }
        ]
    }
