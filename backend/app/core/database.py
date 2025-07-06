from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from pymongo import MongoClient
from redis import Redis
from elasticsearch import Elasticsearch
import structlog
from typing import Generator
import asyncio

from app.core.config import settings

logger = structlog.get_logger()

# PostgreSQL Database
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Database
mongo_client = MongoClient(settings.MONGODB_URL)
mongo_db = mongo_client.get_default_database()

# Redis Cache
redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

# Elasticsearch
es_client = Elasticsearch([settings.ELASTICSEARCH_URL])

def get_db() -> Generator[Session, None, None]:
    """Get PostgreSQL database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("Database session error", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()

def get_mongo_db():
    """Get MongoDB database instance"""
    return mongo_db

def get_redis_client():
    """Get Redis client"""
    return redis_client

def get_elasticsearch_client():
    """Get Elasticsearch client"""
    return es_client

async def init_db():
    """Initialize database connections and create tables"""
    try:
        # Test PostgreSQL connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("PostgreSQL connection established")
        
        # Test MongoDB connection
        mongo_client.admin.command('ping')
        logger.info("MongoDB connection established")
        
        # Test Redis connection
        redis_client.ping()
        logger.info("Redis connection established")
        
        # Test Elasticsearch connection
        if es_client.ping():
            logger.info("Elasticsearch connection established")
        else:
            logger.warning("Elasticsearch connection failed")
        
        # Create PostgreSQL tables
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL tables created")
        
        # Initialize Elasticsearch indices
        await init_elasticsearch_indices()
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        raise

async def init_elasticsearch_indices():
    """Initialize Elasticsearch indices for OSINT data"""
    try:
        # Person index
        person_mapping = {
            "mappings": {
                "properties": {
                    "name": {"type": "text", "analyzer": "standard"},
                    "aliases": {"type": "text", "analyzer": "standard"},
                    "email": {"type": "keyword"},
                    "phone": {"type": "keyword"},
                    "location": {"type": "geo_point"},
                    "social_profiles": {"type": "object"},
                    "professional_info": {"type": "object"},
                    "digital_footprint": {"type": "object"},
                    "behavioral_patterns": {"type": "object"},
                    "risk_score": {"type": "float"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        # Organization index
        organization_mapping = {
            "mappings": {
                "properties": {
                    "name": {"type": "text", "analyzer": "standard"},
                    "type": {"type": "keyword"},
                    "industry": {"type": "keyword"},
                    "location": {"type": "geo_point"},
                    "employees": {"type": "integer"},
                    "website": {"type": "keyword"},
                    "social_profiles": {"type": "object"},
                    "financial_info": {"type": "object"},
                    "risk_score": {"type": "float"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        # Event index
        event_mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "standard"},
                    "description": {"type": "text", "analyzer": "standard"},
                    "type": {"type": "keyword"},
                    "location": {"type": "geo_point"},
                    "date": {"type": "date"},
                    "participants": {"type": "object"},
                    "sources": {"type": "object"},
                    "sentiment": {"type": "float"},
                    "impact_score": {"type": "float"},
                    "created_at": {"type": "date"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        # Social media posts index
        social_post_mapping = {
            "mappings": {
                "properties": {
                    "platform": {"type": "keyword"},
                    "author": {"type": "text", "analyzer": "standard"},
                    "content": {"type": "text", "analyzer": "standard"},
                    "language": {"type": "keyword"},
                    "sentiment": {"type": "float"},
                    "engagement": {"type": "object"},
                    "location": {"type": "geo_point"},
                    "posted_at": {"type": "date"},
                    "created_at": {"type": "date"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        # Create indices
        indices = [
            ("indosint_persons", person_mapping),
            ("indosint_organizations", organization_mapping),
            ("indosint_events", event_mapping),
            ("indosint_social_posts", social_post_mapping)
        ]
        
        for index_name, mapping in indices:
            if not es_client.indices.exists(index=index_name):
                es_client.indices.create(index=index_name, body=mapping)
                logger.info(f"Created Elasticsearch index: {index_name}")
            else:
                logger.info(f"Elasticsearch index already exists: {index_name}")
                
    except Exception as e:
        logger.error("Elasticsearch initialization failed", error=str(e))
        raise

def close_db_connections():
    """Close all database connections"""
    try:
        mongo_client.close()
        redis_client.close()
        es_client.close()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error("Error closing database connections", error=str(e)) 