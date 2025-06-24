"""
Data loader to import brand mention data from JSON into SQLite
"""

import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables, BrandMention, BrandSummary
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_json_data(json_file_path: str) -> dict:
    """Load and validate JSON data from scraper output"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate required fields for the new structure
        required_fields = ['comprehensive_analysis', 'summary']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        logger.info(f"✅ Successfully loaded JSON data from {json_file_path}")
        logger.info(f"   Total responses: {data['summary']['total_responses_processed']}")
        logger.info(f"   Total mentions: {data['summary']['grand_total_mentions']}")
        
        return data
    
    except FileNotFoundError:
        logger.error(f"❌ JSON file not found: {json_file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON format: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Error loading JSON data: {e}")
        raise


def clear_existing_data(db: Session):
    """Clear existing data from database tables"""
    try:
        db.query(BrandMention).delete()
        db.query(BrandSummary).delete()
        db.commit()
        logger.info("🗑️  Cleared existing data from database")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error clearing existing data: {e}")
        raise


def load_brand_mentions(db: Session, data: dict):
    """Load individual brand mentions into database"""
    try:
        mentions_added = 0
        
        # Extract response analysis from the new structure
        response_analysis = data['comprehensive_analysis']['response_analysis']
        
        for response_data in response_analysis:
            prompt_id = response_data['response_number']
            prompt_text = response_data['prompt']
            response_length = response_data['response_length']
            
            # For SQLite, we'll use a placeholder response text since it's not in the summary
            response_text = f"Response to: {prompt_text} (Length: {response_length} chars)"
            
            # Extract brand mentions from this response
            for brand, count in response_data['brand_breakdown'].items():
                if count > 0:  # Only add if brand was mentioned
                    mention = BrandMention(
                        brand=brand,
                        count=count,
                        prompt_id=prompt_id,
                        prompt_text=prompt_text,
                        response_text=response_text,
                        response_length=response_length
                    )
                    db.add(mention)
                    mentions_added += 1
        
        db.commit()
        logger.info(f"✅ Added {mentions_added} brand mention records")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error loading brand mentions: {e}")
        raise


def load_brand_summaries(db: Session, data: dict):
    """Load aggregated brand summaries into database"""
    try:
        summaries_added = 0
        total_mentions = data['summary']['grand_total_mentions']
        total_responses = data['summary']['total_responses_processed']
        
        # Extract brand analysis from the new structure
        brand_analysis = data['comprehensive_analysis']['brand_analysis']
        
        for brand, brand_data in brand_analysis.items():
            brand_total = brand_data['total_mentions']
            
            # Calculate metrics from the data
            avg_mentions = brand_data['avg_per_response']
            max_mentions = brand_data['max_in_single_response']
            percentage = brand_data['percentage']
            
            summary = BrandSummary(
                brand=brand,
                total_mentions=brand_total,
                total_responses=total_responses,
                avg_mentions_per_response=round(avg_mentions, 2),
                max_mentions_single_response=max_mentions,
                percentage_of_total=round(percentage, 2)
            )
            db.add(summary)
            summaries_added += 1
        
        db.commit()
        logger.info(f"✅ Added {summaries_added} brand summary records")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error loading brand summaries: {e}")
        raise


def find_latest_json_file() -> str:
    """Find the most recent JSON file from the scraper"""
    try:
        # Look in stage1_scraper directory
        stage1_dir = "../stage1_scraper"
        if not os.path.exists(stage1_dir):
            stage1_dir = "."
        
        json_files = []
        for file in os.listdir(stage1_dir):
            if file.endswith('.json') and ('brand_mentions' in file or 'results' in file):
                file_path = os.path.join(stage1_dir, file)
                file_stat = os.stat(file_path)
                json_files.append((file_path, file_stat.st_mtime))
        
        if not json_files:
            raise FileNotFoundError("No JSON result files found")
        
        # Sort by modification time and get the latest
        json_files.sort(key=lambda x: x[1], reverse=True)
        latest_file = json_files[0][0]
        
        logger.info(f"📄 Found latest JSON file: {latest_file}")
        return latest_file
        
    except Exception as e:
        logger.error(f"❌ Error finding JSON file: {e}")
        raise


def load_data_to_database(json_file_path: str = None, clear_existing: bool = True):
    """Main function to load data from JSON into SQLite"""
    try:
        # Create tables if they don't exist
        create_tables()
        logger.info("📋 Database tables ready")
        
        # Find JSON file if not provided
        if json_file_path is None:
            json_file_path = find_latest_json_file()
        
        # Load JSON data
        data = load_json_data(json_file_path)
        
        # Create database session
        db = SessionLocal()
        
        try:
            # Clear existing data if requested
            if clear_existing:
                clear_existing_data(db)
            
            # Load brand mentions
            load_brand_mentions(db, data)
            
            # Load brand summaries
            load_brand_summaries(db, data)
            
            logger.info("🎉 Data loading completed successfully!")
            
            # Print summary
            total_mentions = db.query(BrandMention).count()
            total_summaries = db.query(BrandSummary).count()
            logger.info(f"📊 Database Summary:")
            logger.info(f"   - Brand mention records: {total_mentions}")
            logger.info(f"   - Brand summary records: {total_summaries}")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"❌ Data loading failed: {e}")
        raise


if __name__ == "__main__":
    import sys
    
    # Allow passing JSON file path as command line argument
    json_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        load_data_to_database(json_file)
    except Exception as e:
        logger.error(f"❌ Failed to load data: {e}")
        sys.exit(1) 