from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="viewer")  # super_admin, admin, analyst, investigator, viewer
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Profile information
    phone = Column(String(20))
    organization = Column(String(100))
    department = Column(String(100))
    position = Column(String(100))
    
    # Preferences
    language_preference = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    notification_settings = Column(JSON, default={})
    
    # Security
    api_key = Column(String(255))
    last_login = Column(DateTime(timezone=True))
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)
    
    # Relationships
    search_history = relationship("SearchHistory", back_populates="user")
    reports = relationship("Report", back_populates="created_by_user")
    investigations = relationship("Investigation", back_populates="assigned_to_user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    @property
    def permissions(self):
        """Get user permissions based on role"""
        role_permissions = {
            "super_admin": [
                "read_all", "write_all", "delete_all", "manage_users",
                "osint_collection", "analysis", "reports", "system_config",
                "data_export", "api_access", "audit_logs"
            ],
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
        return role_permissions.get(self.role, [])
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions
    
    def can_access_data(self, data_owner_id: int = None) -> bool:
        """Check if user can access specific data"""
        if self.role in ["super_admin", "admin", "analyst"]:
            return True
        elif self.role == "investigator":
            # Investigators can access data assigned to them
            return data_owner_id == self.id
        else:
            # Viewers have limited access
            return False 