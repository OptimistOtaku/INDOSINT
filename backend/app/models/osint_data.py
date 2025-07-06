from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    aliases = Column(JSON)  # List of alternative names
    email = Column(String(100), index=True)
    phone = Column(String(20), index=True)
    
    # Location information
    location = Column(JSON)  # {lat, lng, address, city, state, country}
    
    # Social media profiles
    social_profiles = Column(JSON)  # {platform: profile_url}
    
    # Professional information
    professional_info = Column(JSON)  # {company, position, skills, education}
    
    # Digital footprint
    digital_footprint = Column(JSON)  # {websites, online_presence, etc.}
    
    # Behavioral patterns
    behavioral_patterns = Column(JSON)  # {activity_patterns, interests, etc.}
    
    # Risk assessment
    risk_score = Column(Float, default=0.0)
    risk_factors = Column(JSON)
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    data_sources = Column(JSON)  # List of sources
    tags = Column(JSON)  # List of tags
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    relationships = relationship("Relationship", back_populates="person")
    events = relationship("EventParticipant", back_populates="person")
    
    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}')>"

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(50))  # company, government, ngo, etc.
    industry = Column(String(100))
    
    # Location information
    location = Column(JSON)  # {lat, lng, address, city, state, country}
    
    # Company information
    website = Column(String(200))
    employees = Column(Integer)
    founded_year = Column(Integer)
    
    # Social media profiles
    social_profiles = Column(JSON)
    
    # Financial information
    financial_info = Column(JSON)  # {revenue, funding, etc.}
    
    # Risk assessment
    risk_score = Column(Float, default=0.0)
    risk_factors = Column(JSON)
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    data_sources = Column(JSON)
    tags = Column(JSON)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    relationships = relationship("Relationship", back_populates="organization")
    events = relationship("EventParticipant", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    type = Column(String(50))  # meeting, conference, incident, etc.
    
    # Location information
    location = Column(JSON)
    
    # Timing
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # Participants
    participants = Column(JSON)  # List of participant IDs
    
    # Sources
    sources = Column(JSON)  # List of source URLs
    
    # Analysis
    sentiment = Column(Float)  # -1 to 1
    impact_score = Column(Float, default=0.0)
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    tags = Column(JSON)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    event_participants = relationship("EventParticipant", back_populates="event")
    
    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}')>"

class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, index=True)  # twitter, linkedin, etc.
    post_id = Column(String(100), index=True)  # Original post ID from platform
    author = Column(String(100), index=True)
    content = Column(Text)
    language = Column(String(10))
    
    # Engagement metrics
    engagement = Column(JSON)  # {likes, shares, comments, etc.}
    
    # Location
    location = Column(JSON)
    
    # Analysis
    sentiment = Column(Float)
    topics = Column(JSON)  # Extracted topics
    entities = Column(JSON)  # Named entities
    
    # Timing
    posted_at = Column(DateTime(timezone=True))
    
    # Metadata
    url = Column(String(500))
    media_urls = Column(JSON)  # List of media URLs
    hashtags = Column(JSON)
    mentions = Column(JSON)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    collected_by = Column(Integer, ForeignKey("users.id"))
    
    def __repr__(self):
        return f"<SocialMediaPost(id={self.id}, platform='{self.platform}', author='{self.author}')>"

class Relationship(Base):
    __tablename__ = "relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    relationship_type = Column(String(50))  # employee, founder, investor, etc.
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    is_current = Column(Boolean, default=True)
    
    # Additional details
    position = Column(String(100))
    description = Column(Text)
    confidence_score = Column(Float, default=0.0)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    person = relationship("Person", back_populates="relationships")
    organization = relationship("Organization", back_populates="relationships")
    
    def __repr__(self):
        return f"<Relationship(id={self.id}, person_id={self.person_id}, org_id={self.organization_id})>"

class EventParticipant(Base):
    __tablename__ = "event_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    person_id = Column(Integer, ForeignKey("persons.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    role = Column(String(50))  # speaker, attendee, organizer, etc.
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="event_participants")
    person = relationship("Person", back_populates="events")
    organization = relationship("Organization", back_populates="events")
    
    def __repr__(self):
        return f"<EventParticipant(id={self.id}, event_id={self.event_id})>"

class DigitalDNA(Base):
    __tablename__ = "digital_dna"
    
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), unique=True)
    
    # Behavioral patterns
    writing_style = Column(JSON)  # Writing patterns, vocabulary, etc.
    posting_patterns = Column(JSON)  # Timing, frequency, etc.
    interaction_patterns = Column(JSON)  # How they interact with others
    content_preferences = Column(JSON)  # Topics they engage with
    
    # Professional patterns
    career_progression = Column(JSON)
    skill_development = Column(JSON)
    networking_behavior = Column(JSON)
    
    # Digital footprint
    device_fingerprint = Column(JSON)
    location_patterns = Column(JSON)
    online_activity_timing = Column(JSON)
    
    # Communication style
    language_usage = Column(JSON)
    sentiment_patterns = Column(JSON)
    formality_levels = Column(JSON)
    
    # Interest mapping
    topic_preferences = Column(JSON)
    engagement_patterns = Column(JSON)
    influence_networks = Column(JSON)
    
    # Risk indicators
    risk_indicators = Column(JSON)
    anomaly_scores = Column(JSON)
    
    # Metadata
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    confidence_score = Column(Float, default=0.0)
    
    def __repr__(self):
        return f"<DigitalDNA(id={self.id}, person_id={self.person_id})>"

# Create indexes for better performance
Index('idx_persons_name', Person.name)
Index('idx_persons_email', Person.email)
Index('idx_organizations_name', Organization.name)
Index('idx_events_title', Event.title)
Index('idx_social_posts_platform_author', SocialMediaPost.platform, SocialMediaPost.author)
Index('idx_social_posts_posted_at', SocialMediaPost.posted_at) 