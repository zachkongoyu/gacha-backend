"""Asset service main application for CDN and asset URLs."""
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from shared.settings import settings
from shared.database import create_db_pool, close_db_pool


app = FastAPI(
    title="Asset Service",
    description="Asset and CDN URL management service",
    version="0.1.0"
)


class AssetResponse(BaseModel):
    """Asset URL response."""
    asset_id: str
    asset_type: str
    url: str
    cdn_url: str
    thumbnail_url: Optional[str] = None


class AssetBatch(BaseModel):
    """Batch asset response."""
    assets: List[AssetResponse]
    total: int


@app.on_event("startup")
async def startup_event():
    """Initialize database pool on startup."""
    await create_db_pool()


@app.on_event("shutdown")
async def shutdown_event():
    """Close database pool on shutdown."""
    await close_db_pool()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": "asset", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/assets/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: str):
    """
    Get asset URL by asset ID.
    
    Args:
        asset_id: Asset identifier
        
    Returns:
        Asset URLs (original, CDN, thumbnail)
    """
    # Stub asset URL generation
    return AssetResponse(
        asset_id=asset_id,
        asset_type="image",
        url=f"https://storage.example.com/assets/{asset_id}.png",
        cdn_url=f"https://cdn.example.com/assets/{asset_id}.png",
        thumbnail_url=f"https://cdn.example.com/assets/{asset_id}_thumb.png"
    )


@app.get("/assets", response_model=AssetBatch)
async def list_assets(
    asset_type: Optional[str] = Query(None, description="Filter by asset type"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, ge=1, le=1000, description="Number of assets to return")
):
    """
    List available assets with filters.
    
    Args:
        asset_type: Optional filter by type (image, video, audio, model)
        category: Optional filter by category (character, weapon, background)
        limit: Maximum number of results
        
    Returns:
        List of assets
    """
    # Stub asset list
    stub_assets = [
        AssetResponse(
            asset_id="char_001",
            asset_type="image",
            url="https://storage.example.com/assets/char_001.png",
            cdn_url="https://cdn.example.com/assets/char_001.png",
            thumbnail_url="https://cdn.example.com/assets/char_001_thumb.png"
        ),
        AssetResponse(
            asset_id="weapon_001",
            asset_type="image",
            url="https://storage.example.com/assets/weapon_001.png",
            cdn_url="https://cdn.example.com/assets/weapon_001.png",
            thumbnail_url="https://cdn.example.com/assets/weapon_001_thumb.png"
        ),
        AssetResponse(
            asset_id="bg_001",
            asset_type="image",
            url="https://storage.example.com/assets/bg_001.png",
            cdn_url="https://cdn.example.com/assets/bg_001.png",
            thumbnail_url="https://cdn.example.com/assets/bg_001_thumb.png"
        ),
    ]
    
    # Apply filters
    assets = stub_assets[:limit]
    
    return AssetBatch(
        assets=assets,
        total=len(assets)
    )


@app.post("/assets/upload")
async def upload_asset(
    asset_type: str,
    category: str
):
    """
    Upload a new asset (stub - returns upload URL).
    
    Args:
        asset_type: Type of asset (image, video, audio, model)
        category: Category (character, weapon, background, etc.)
        
    Returns:
        Upload URL and asset ID
    """
    import uuid
    
    asset_id = str(uuid.uuid4())
    
    # Stub upload URL generation
    return {
        "asset_id": asset_id,
        "upload_url": f"https://upload.example.com/assets/{asset_id}",
        "expires_at": "2026-01-08T17:00:00Z",
        "method": "PUT",
        "headers": {
            "Content-Type": f"{asset_type}/*"
        }
    }


@app.get("/assets/{asset_id}/versions")
async def list_asset_versions(asset_id: str):
    """
    List versions of an asset.
    
    Args:
        asset_id: Asset identifier
        
    Returns:
        Asset version history
    """
    # Stub version list
    return {
        "asset_id": asset_id,
        "versions": [
            {
                "version_id": "v1",
                "url": f"https://cdn.example.com/assets/{asset_id}_v1.png",
                "created_at": "2026-01-01T00:00:00Z",
                "size_bytes": 1024000
            },
            {
                "version_id": "v2",
                "url": f"https://cdn.example.com/assets/{asset_id}_v2.png",
                "created_at": "2026-01-05T00:00:00Z",
                "size_bytes": 1048576,
                "is_current": True
            }
        ]
    }


@app.delete("/assets/{asset_id}")
async def delete_asset(asset_id: str):
    """
    Delete an asset.
    
    Args:
        asset_id: Asset identifier
        
    Returns:
        Deletion confirmation
    """
    # Stub deletion
    return {
        "asset_id": asset_id,
        "deleted": True,
        "message": "Asset marked for deletion"
    }
