from app import db
from datetime import datetime
import uuid

class Organization(db.Model):
    __tablename__ = 'organizations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    domain = db.Column(db.String(100), unique=True)
    logo_url = db.Column(db.String(500))
    website = db.Column(db.String(500))
    contact_email = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    industry = db.Column(db.String(100))
    size = db.Column(db.String(50))  # small, medium, large
    subscription_plan = db.Column(db.String(50), default='basic')  # basic, pro, enterprise
    subscription_status = db.Column(db.String(20), default='active')  # active, suspended, cancelled
    max_users = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = db.relationship('UserOrganization', backref='organization', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'domain': self.domain,
            'logo_url': self.logo_url,
            'website': self.website,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'industry': self.industry,
            'size': self.size,
            'subscription_plan': self.subscription_plan,
            'subscription_status': self.subscription_status,
            'max_users': self.max_users,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class UserOrganization(db.Model):
    __tablename__ = 'user_organizations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    role = db.Column(db.String(50), default='member')  # owner, admin, member, viewer
    is_active = db.Column(db.Boolean, default=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'role': self.role,
            'is_active': self.is_active,
            'joined_at': self.joined_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 