"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class BrandMentionResponse(BaseModel):
    """Response model for individual brand mention"""
    brand: str
    total_mentions: int
    total_responses: int
    avg_mentions_per_response: float
    max_mentions_single_response: int
    percentage_of_total: float
    last_updated: datetime

    class Config:
        from_attributes = True


class BrandSummaryResponse(BaseModel):
    """Response model for /mentions endpoint"""
    total_mentions: int
    total_responses: int
    analysis_date: datetime
    brands: List[BrandMentionResponse]

    class Config:
        from_attributes = True


class SingleBrandResponse(BaseModel):
    """Response model for /mentions/{brand} endpoint"""
    brand: str
    total_mentions: int
    exists: bool = True

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    message: str
    status_code: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    database_connected: bool
    total_records: int 