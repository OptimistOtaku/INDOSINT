from app import db
from datetime import datetime
import json
import enum

class SearchType(enum.Enum):
    SOCIAL_MEDIA = "social_media"
    DIGITAL_FOOTPRINT = "digital_footprint"
    FACE_RECOGNITION = "face_recognition"
    DOMAIN_SEARCH = "domain_search"
    EMAIL_BREACH = "email_breach"
    NEWS_SEARCH = "news_search"
    GOVERNMENT_RECORDS = "government_records"

class SearchStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_type = db.Column(db.Enum(SearchType), nullable=False)
    query = db.Column(db.String(500), nullable=False)
    parameters = db.Column(db.Text)  # JSON object of search parameters
    results_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum(SearchStatus), default=SearchStatus.PENDING)
    results_summary = db.Column(db.Text)  # JSON summary of results
    execution_time = db.Column(db.Float)  # Time taken in seconds
    error_message = db.Column(db.Text)
    language = db.Column(db.String(10), default='en')
    platforms = db.Column(db.Text)  # JSON array of platforms searched
    confidence_threshold = db.Column(db.Float, default=0.5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def set_parameters(self, params):
        self.parameters = json.dumps(params)
    
    def get_parameters(self):
        return json.loads(self.parameters) if self.parameters else {}
    
    def set_results_summary(self, summary):
        self.results_summary = json.dumps(summary)
    
    def get_results_summary(self):
        return json.loads(self.results_summary) if self.results_summary else {}
    
    def set_platforms(self, platforms):
        self.platforms = json.dumps(platforms)
    
    def get_platforms(self):
        return json.loads(self.platforms) if self.platforms else []
    
    def mark_completed(self, results_count=None, execution_time=None):
        self.status = SearchStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        if results_count is not None:
            self.results_count = results_count
        if execution_time is not None:
            self.execution_time = execution_time
    
    def mark_failed(self, error_message):
        self.status = SearchStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'search_type': self.search_type.value,
            'query': self.query,
            'parameters': self.get_parameters(),
            'results_count': self.results_count,
            'status': self.status.value,
            'results_summary': self.get_results_summary(),
            'execution_time': self.execution_time,
            'error_message': self.error_message,
            'language': self.language,
            'platforms': self.get_platforms(),
            'confidence_threshold': self.confidence_threshold,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<SearchHistory {self.search_type.value}: {self.query}>' 