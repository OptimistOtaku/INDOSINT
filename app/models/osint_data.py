from app import db
from datetime import datetime
import uuid
import json

class OSINTData(db.Model):
    __tablename__ = 'osint_data'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    search_query = db.Column(db.String(500), nullable=False)
    data_type = db.Column(db.String(50), nullable=False)  # social_media, digital_footprint, face_recognition, etc.
    source = db.Column(db.String(100), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    confidence_score = db.Column(db.Float, default=0.0)
    language = db.Column(db.String(10), default='en')
    location = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata
    tags = db.Column(db.JSON, default=list)
    is_verified = db.Column(db.Boolean, default=False)
    verification_source = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'search_query': self.search_query,
            'data_type': self.data_type,
            'source': self.source,
            'content': self.content,
            'confidence_score': self.confidence_score,
            'language': self.language,
            'location': self.location,
            'timestamp': self.timestamp.isoformat(),
            'tags': self.tags,
            'is_verified': self.is_verified,
            'verification_source': self.verification_source,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String(500), nullable=False)
    search_type = db.Column(db.String(50), nullable=False)  # social_media, digital_footprint, face_recognition, etc.
    filters = db.Column(db.JSON, default=dict)
    results_count = db.Column(db.Integer, default=0)
    execution_time = db.Column(db.Float)  # in seconds
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'query': self.query,
            'search_type': self.search_type,
            'filters': self.filters,
            'results_count': self.results_count,
            'execution_time': self.execution_time,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Analytics(db.Model):
    __tablename__ = 'analytics'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    analytics_type = db.Column(db.String(50), nullable=False)  # search_trends, user_activity, data_insights
    data = db.Column(db.JSON, nullable=False)
    period = db.Column(db.String(20), default='daily')  # hourly, daily, weekly, monthly
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analytics_type': self.analytics_type,
            'data': self.data,
            'period': self.period,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'created_at': self.created_at.isoformat()
        } 