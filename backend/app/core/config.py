from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "INDOSINT"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_SECRET: str = "your-jwt-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: str = "postgresql://indosint_user:indosint_password@localhost:5432/indosint"
    MONGODB_URL: str = "mongodb://indosint_user:indosint_password@localhost:27017/indosint?authSource=admin"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX_PREFIX: str = "indosint"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: List[str] = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx", "txt"]
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_CLOUD_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    
    # Social Media APIs
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    
    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None
    
    FACEBOOK_APP_ID: Optional[str] = None
    FACEBOOK_APP_SECRET: Optional[str] = None
    
    INSTAGRAM_USERNAME: Optional[str] = None
    INSTAGRAM_PASSWORD: Optional[str] = None
    
    # AWS S3 (for file storage)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_S3_REGION: str = "us-east-1"
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/indosint.log"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # ML Models
    ML_MODELS_DIR: str = "ml_models"
    FACE_RECOGNITION_MODEL: str = "face_recognition_models"
    NLP_MODELS_DIR: str = "nlp_models"
    
    # Supported Languages
    SUPPORTED_LANGUAGES: List[str] = [
        "en", "hi", "bn", "ta", "te", "mr", "gu"
    ]
    
    # Data Sources Configuration
    DATA_SOURCES: dict = {
        "social_media": {
            "twitter": {"enabled": True, "rate_limit": 300},
            "linkedin": {"enabled": True, "rate_limit": 100},
            "facebook": {"enabled": True, "rate_limit": 200},
            "instagram": {"enabled": True, "rate_limit": 100},
            "sharechat": {"enabled": True, "rate_limit": 50},
            "koo": {"enabled": True, "rate_limit": 50}
        },
        "professional": {
            "naukri": {"enabled": True, "rate_limit": 100},
            "monster": {"enabled": True, "rate_limit": 100},
            "linkedin_jobs": {"enabled": True, "rate_limit": 50}
        },
        "government": {
            "voter_records": {"enabled": False, "rate_limit": 10},
            "company_registry": {"enabled": False, "rate_limit": 10},
            "court_records": {"enabled": False, "rate_limit": 10}
        },
        "news": {
            "times_of_india": {"enabled": True, "rate_limit": 100},
            "hindustan_times": {"enabled": True, "rate_limit": 100},
            "the_hindu": {"enabled": True, "rate_limit": 100},
            "regional_news": {"enabled": True, "rate_limit": 50}
        }
    }
    
    # Privacy and Compliance
    DATA_RETENTION_DAYS: int = 90
    ANONYMIZE_PII: bool = True
    GDPR_COMPLIANT: bool = True
    
    # Performance
    MAX_CONCURRENT_REQUESTS: int = 100
    REQUEST_TIMEOUT: int = 30
    CACHE_TTL: int = 3600  # 1 hour
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Create necessary directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.ML_MODELS_DIR, exist_ok=True)
os.makedirs(settings.NLP_MODELS_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True) 