"""
Database configuration and models for Brand Mentions API
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

# Database URL - Using PostgreSQL as required by Bear AI
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ishanahluwalia@localhost:5432/brand_mentions")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class BrandMention(Base):
    """Brand mention model for storing scraped data"""
    __tablename__ = "brand_mentions"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    prompt_id = Column(Integer, nullable=False)
    prompt_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    response_length = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class BrandSummary(Base):
    """Aggregated brand summary for quick queries"""
    __tablename__ = "brand_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, unique=True, index=True, nullable=False)
    total_mentions = Column(Integer, nullable=False, default=0)
    total_responses = Column(Integer, nullable=False, default=0)
    avg_mentions_per_response = Column(Float, nullable=False, default=0.0)
    max_mentions_single_response = Column(Integer, nullable=False, default=0)
    percentage_of_total = Column(Float, nullable=False, default=0.0)
    last_updated = Column(DateTime, server_default=func.now())


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 