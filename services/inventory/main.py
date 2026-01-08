"""Inventory service main application."""
from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

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
    title="Inventory Service",
    description="User inventory management service",
    version="0.1.0",
    lifespan=lifespan
)


class InventoryItem(BaseModel):
    """Inventory item model."""
    item_id: str
    item_name: str
    item_type: str
    rarity: str
    quantity: int
    acquired_at: str


class InventoryResponse(BaseModel):
    """Inventory list response."""
    user_id: str
    items: List[InventoryItem]
    total_items: int


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": "inventory", "status": "running"}


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


@app.get("/inventory", response_model=InventoryResponse)
async def list_inventory(
    item_type: Optional[str] = None,
    rarity: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """
    List user's inventory items.
    
    Args:
        item_type: Optional filter by item type (character, weapon, material)
        rarity: Optional filter by rarity (3-star, 4-star, 5-star)
        authorization: JWT token in Authorization header
        
    Returns:
        User's inventory items
    """
    user_id = get_current_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Stub inventory data (in real implementation, fetch from database)
    stub_items = [
        InventoryItem(
            item_id="item_001",
            item_name="Starter Sword",
            item_type="weapon",
            rarity="3-star",
            quantity=1,
            acquired_at="2026-01-01T00:00:00Z"
        ),
        InventoryItem(
            item_id="item_002",
            item_name="Common Character",
            item_type="character",
            rarity="4-star",
            quantity=1,
            acquired_at="2026-01-02T00:00:00Z"
        ),
        InventoryItem(
            item_id="item_003",
            item_name="Enhancement Material",
            item_type="material",
            rarity="3-star",
            quantity=50,
            acquired_at="2026-01-03T00:00:00Z"
        ),
    ]
    
    # Apply filters
    items = stub_items
    if item_type:
        items = [item for item in items if item.item_type == item_type]
    if rarity:
        items = [item for item in items if item.rarity == rarity]
    
    return InventoryResponse(
        user_id=user_id,
        items=items,
        total_items=len(items)
    )


@app.get("/inventory/{item_id}")
async def get_item(
    item_id: str,
    authorization: Optional[str] = Header(None)
):
    """
    Get details of a specific inventory item.
    
    Args:
        item_id: Item ID
        authorization: JWT token in Authorization header
        
    Returns:
        Item details
    """
    user_id = get_current_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Stub item data
    return {
        "item_id": item_id,
        "item_name": "Sample Item",
        "item_type": "weapon",
        "rarity": "4-star",
        "quantity": 1,
        "level": 1,
        "max_level": 90,
        "stats": {
            "attack": 42,
            "defense": 10
        },
        "acquired_at": "2026-01-01T00:00:00Z"
    }


@app.post("/inventory/{item_id}/enhance")
async def enhance_item(
    item_id: str,
    authorization: Optional[str] = Header(None)
):
    """
    Enhance/level up an inventory item.
    
    Args:
        item_id: Item ID to enhance
        authorization: JWT token in Authorization header
        
    Returns:
        Enhanced item details
    """
    user_id = get_current_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Stub enhancement result
    return {
        "item_id": item_id,
        "previous_level": 1,
        "new_level": 2,
        "stats_increased": {
            "attack": 5,
            "defense": 2
        },
        "success": True
    }
