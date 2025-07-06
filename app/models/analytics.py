from app import db
from datetime import datetime
import json
import enum

class AnalyticsType(enum.Enum):
    USER_ACTIVITY = "user_activity"
    SEARCH_PATTERNS = "search_patterns"
    RISK_ANALYSIS = "risk_analysis"
    PLATFORM_USAGE = "platform_usage"
    LANGUAGE_DISTRIBUTION = "language_distribution"
    TREND_ANALYSIS = "trend_analysis"
    PERFORMANCE_METRICS = "performance_metrics"

class AnalyticsData(db.Model):
    __tablename__ = 'analytics_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    analytics_type = db.Column(db.Enum(AnalyticsType), nullable=False)
    data = db.Column(db.Text)  # JSON data
    insights = db.Column(db.Text)  # JSON insights
    metrics = db.Column(db.Text)  # JSON metrics
    time_period = db.Column(db.String(50))  # e.g., "daily", "weekly", "monthly"
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_data(self, data):
        self.data = json.dumps(data)
    
    def get_data(self):
        return json.loads(self.data) if self.data else {}
    
    def set_insights(self, insights):
        self.insights = json.dumps(insights)
    
    def get_insights(self):
        return json.loads(self.insights) if self.insights else {}
    
    def set_metrics(self, metrics):
        self.metrics = json.dumps(metrics)
    
    def get_metrics(self):
        return json.loads(self.metrics) if self.metrics else {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analytics_type': self.analytics_type.value,
            'data': self.get_data(),
            'insights': self.get_insights(),
            'metrics': self.get_metrics(),
            'time_period': self.time_period,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<AnalyticsData {self.analytics_type.value}>' 