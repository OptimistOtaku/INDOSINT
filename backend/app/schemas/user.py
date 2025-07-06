from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "viewer"
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    organization: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    language_preference: Optional[str] = "en"
    timezone: Optional[str] = "UTC"
    notification_settings: Optional[Dict[str, Any]] = {}

class UserResponse(UserBase):
    id: int
    phone: Optional[str] = None
    organization: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    language_preference: str = "en"
    timezone: str = "UTC"
    notification_settings: Dict[str, Any] = {}
    is_verified: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    phone: Optional[str] = None
    organization: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    language_preference: str
    timezone: str
    notification_settings: Dict[str, Any]
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserList(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool
    organization: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserPermissions(BaseModel):
    permissions: List[str]
    role: str
    
    class Config:
        from_attributes = True

class UserStats(BaseModel):
    total_searches: int
    total_reports: int
    total_investigations: int
    last_activity: Optional[datetime] = None
    
    class Config:
        from_attributes = True 