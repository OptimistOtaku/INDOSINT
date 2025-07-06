from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import structlog
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import TokenData

logger = structlog.get_logger()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        return token_data
    except JWTError as e:
        logger.error("JWT token verification failed", error=str(e))
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        token_data = verify_token(token)
        if token_data is None:
            raise credentials_exception
        
        user = db.query(User).filter(User.username == token_data.username).first()
        if user is None:
            raise credentials_exception
        
        return user
    except Exception as e:
        logger.error("Authentication failed", error=str(e))
        raise credentials_exception

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def check_permissions(user: User, required_permissions: list) -> bool:
    """Check if user has required permissions"""
    if not user.is_active:
        return False
    
    # Super admin has all permissions
    if user.role == "super_admin":
        return True
    
    # Check role-based permissions
    role_permissions = {
        "admin": [
            "read_all", "write_all", "delete_all", "manage_users",
            "osint_collection", "analysis", "reports", "system_config"
        ],
        "analyst": [
            "read_all", "write_analysis", "osint_collection", 
            "analysis", "reports", "basic_search"
        ],
        "investigator": [
            "read_assigned", "write_assigned", "osint_collection",
            "analysis", "reports", "basic_search"
        ],
        "viewer": [
            "read_assigned", "basic_search", "view_reports"
        ]
    }
    
    user_permissions = role_permissions.get(user.role, [])
    return all(perm in user_permissions for perm in required_permissions)

def require_permissions(required_permissions: list):
    """Decorator to require specific permissions"""
    def permission_checker(current_user: User = Depends(get_current_active_user)):
        if not check_permissions(current_user, required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return permission_checker

# Permission decorators
require_admin = require_permissions(["manage_users", "system_config"])
require_analyst = require_permissions(["analysis", "reports"])
require_investigator = require_permissions(["osint_collection", "analysis"])
require_viewer = require_permissions(["basic_search"])

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def generate_api_key(user_id: int) -> str:
    """Generate API key for user"""
    data = {
        "user_id": user_id,
        "type": "api_key",
        "created_at": datetime.utcnow().isoformat()
    }
    return jwt.encode(data, settings.JWT_SECRET, algorithm="HS256")

def verify_api_key(api_key: str) -> Optional[int]:
    """Verify API key and return user ID"""
    try:
        payload = jwt.decode(api_key, settings.JWT_SECRET, algorithms=["HS256"])
        if payload.get("type") != "api_key":
            return None
        return payload.get("user_id")
    except JWTError:
        return None

# Rate limiting
class RateLimiter:
    """Simple rate limiter using Redis"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, key: str, limit: int, window: int = 60) -> bool:
        """Check if request is allowed within rate limit"""
        current = self.redis.get(key)
        if current is None:
            self.redis.setex(key, window, 1)
            return True
        
        count = int(current)
        if count >= limit:
            return False
        
        self.redis.incr(key)
        return True
    
    def get_remaining(self, key: str) -> int:
        """Get remaining requests for a key"""
        current = self.redis.get(key)
        if current is None:
            return settings.RATE_LIMIT_PER_MINUTE
        return max(0, settings.RATE_LIMIT_PER_MINUTE - int(current))

# Security headers middleware
def add_security_headers(response):
    """Add security headers to response"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response

# Input validation and sanitization
def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    import re
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_str)
    return sanitized.strip()

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate Indian phone number format"""
    import re
    # Indian phone number patterns
    patterns = [
        r'^\+91[0-9]{10}$',  # +91XXXXXXXXXX
        r'^[0-9]{10}$',      # XXXXXXXXXX
        r'^[0-9]{12}$'       # XXXXXXXXXXXX
    ]
    return any(re.match(pattern, phone) for pattern in patterns)

# Audit logging
def log_security_event(event_type: str, user_id: Optional[int], details: dict):
    """Log security events for audit purposes"""
    logger.info(
        "Security event",
        event_type=event_type,
        user_id=user_id,
        details=details,
        timestamp=datetime.utcnow().isoformat()
    ) 