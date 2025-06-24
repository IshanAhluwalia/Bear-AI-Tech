"""
Brand Mentions API - FastAPI application
Serves brand mention data extracted from ChatGPT responses
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List
import logging

from database import get_db, BrandSummary, BrandMention
from models import (
    BrandSummaryResponse, 
    SingleBrandResponse, 
    BrandMentionResponse,
    HealthResponse,
    ErrorResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Brand Mentions API",
    description="API for querying sportswear brand mentions extracted from ChatGPT responses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Brand Mentions API",
        "description": "API for querying sportswear brand mentions from ChatGPT",
        "version": "1.0.0",
        "endpoints": {
            "GET /mentions": "Get all brand mention summaries",
            "GET /mentions/{brand}": "Get mentions for specific brand",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        },
        "brands_tracked": ["Nike", "Adidas", "Hoka", "New Balance", "Jordan"]
    }


@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        total_records = db.query(BrandMention).count()
        database_connected = True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        database_connected = False
        total_records = 0
    
    return HealthResponse(
        status="healthy" if database_connected else "unhealthy",
        timestamp=datetime.now(),
        database_connected=database_connected,
        total_records=total_records
    )


@app.get("/mentions", response_model=BrandSummaryResponse)
async def get_all_mentions(db: Session = Depends(get_db)):
    """
    Get total mentions for all brands
    
    Returns comprehensive brand mention statistics including:
    - Total mentions per brand
    - Response coverage
    - Percentages and averages
    """
    try:
        # Get all brand summaries
        brand_summaries = db.query(BrandSummary).all()
        
        if not brand_summaries:
            raise HTTPException(
                status_code=404, 
                detail="No brand mention data found. Please ensure data has been loaded."
            )
        
        # Calculate totals
        total_mentions = sum(brand.total_mentions for brand in brand_summaries)
        total_responses = max(brand.total_responses for brand in brand_summaries) if brand_summaries else 0
        
        # Convert to response models
        brand_responses = [
            BrandMentionResponse(
                brand=brand.brand,
                total_mentions=brand.total_mentions,
                total_responses=brand.total_responses,
                avg_mentions_per_response=brand.avg_mentions_per_response,
                max_mentions_single_response=brand.max_mentions_single_response,
                percentage_of_total=brand.percentage_of_total,
                last_updated=brand.last_updated
            )
            for brand in brand_summaries
        ]
        
        # Sort by total mentions (descending)
        brand_responses.sort(key=lambda x: x.total_mentions, reverse=True)
        
        return BrandSummaryResponse(
            total_mentions=total_mentions,
            total_responses=total_responses,
            analysis_date=brand_summaries[0].last_updated if brand_summaries else datetime.now(),
            brands=brand_responses
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_all_mentions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/mentions/{brand}", response_model=SingleBrandResponse)
async def get_brand_mentions(brand: str, db: Session = Depends(get_db)):
    """
    Get mentions for a specific brand
    
    Args:
        brand: Brand name (case-insensitive)
        
    Returns:
        Brand mention count or 404 if brand not found
    """
    try:
        # Case-insensitive brand lookup
        brand_summary = db.query(BrandSummary).filter(
            func.lower(BrandSummary.brand) == brand.lower()
        ).first()
        
        if not brand_summary:
            # Return 404 with proper error response
            raise HTTPException(
                status_code=404,
                detail=f"Brand '{brand}' not found. Available brands: Nike, Adidas, Hoka, New Balance, Jordan"
            )
        
        return SingleBrandResponse(
            brand=brand_summary.brand,
            total_mentions=brand_summary.total_mentions,
            exists=True
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_brand_mentions for {brand}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/mentions/{brand}/details", response_model=BrandMentionResponse)
async def get_brand_details(brand: str, db: Session = Depends(get_db)):
    """
    Get detailed statistics for a specific brand
    
    Args:
        brand: Brand name (case-insensitive)
        
    Returns:
        Detailed brand statistics including averages and percentages
    """
    try:
        brand_summary = db.query(BrandSummary).filter(
            func.lower(BrandSummary.brand) == brand.lower()
        ).first()
        
        if not brand_summary:
            raise HTTPException(
                status_code=404,
                detail=f"Brand '{brand}' not found"
            )
        
        return BrandMentionResponse(
            brand=brand_summary.brand,
            total_mentions=brand_summary.total_mentions,
            total_responses=brand_summary.total_responses,
            avg_mentions_per_response=brand_summary.avg_mentions_per_response,
            max_mentions_single_response=brand_summary.max_mentions_single_response,
            percentage_of_total=brand_summary.percentage_of_total,
            last_updated=brand_summary.last_updated
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_brand_details for {brand}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 