from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

class SearchType(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"
    FACE = "face"
    MULTIMODAL = "multimodal"

class ImageSearchType(str, Enum):
    OBJECT = "object"
    TEXT = "text"
    SCENE = "scene"
    FACE = "face"

class SearchFilters(BaseModel):
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    sources: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    locations: Optional[List[str]] = None
    confidence_min: Optional[float] = Field(None, ge=0.0, le=1.0)
    risk_score_min: Optional[float] = Field(None, ge=0.0, le=1.0)
    tags: Optional[List[str]] = None
    platforms: Optional[List[str]] = None

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    filters: Optional[SearchFilters] = None
    language: Optional[str] = "en"
    limit: Optional[int] = Field(50, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0)

class VoiceSearchRequest(BaseModel):
    audio_data: bytes
    filters: Optional[SearchFilters] = None
    language: Optional[str] = "en"
    limit: Optional[int] = Field(50, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0)

class ImageSearchRequest(BaseModel):
    image_data: bytes
    search_type: ImageSearchType = ImageSearchType.OBJECT
    filters: Optional[SearchFilters] = None
    limit: Optional[int] = Field(50, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0)

class FaceSearchRequest(BaseModel):
    image_data: bytes
    confidence_threshold: Optional[float] = Field(0.8, ge=0.0, le=1.0)
    filters: Optional[SearchFilters] = None
    limit: Optional[int] = Field(20, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0)

class SearchResult(BaseModel):
    id: str
    type: str  # person, organization, event, social_post, etc.
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    source: str
    platform: Optional[str] = None
    language: Optional[str] = None
    location: Optional[Dict[str, Any]] = None
    date: Optional[datetime] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    risk_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    created_at: datetime

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_count: int
    search_type: SearchType
    execution_time: Optional[float] = None
    suggestions: Optional[List[str]] = None

class PersonSearchResult(SearchResult):
    name: str
    aliases: List[str] = []
    email: Optional[str] = None
    phone: Optional[str] = None
    social_profiles: Dict[str, str] = {}
    professional_info: Dict[str, Any] = {}
    behavioral_patterns: Dict[str, Any] = {}

class OrganizationSearchResult(SearchResult):
    name: str
    type: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    employees: Optional[int] = None
    social_profiles: Dict[str, str] = {}
    financial_info: Dict[str, Any] = {}

class EventSearchResult(SearchResult):
    title: str
    description: Optional[str] = None
    type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    participants: List[str] = []
    sentiment: Optional[float] = Field(None, ge=-1.0, le=1.0)
    impact_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class SocialMediaSearchResult(SearchResult):
    platform: str
    author: str
    content: str
    engagement: Dict[str, int] = {}
    hashtags: List[str] = []
    mentions: List[str] = []
    media_urls: List[str] = []
    sentiment: Optional[float] = Field(None, ge=-1.0, le=1.0)
    topics: List[str] = []
    entities: List[str] = []

class FaceSearchResult(SearchResult):
    person_id: Optional[str] = None
    person_name: Optional[str] = None
    face_confidence: float = Field(..., ge=0.0, le=1.0)
    face_features: Dict[str, Any] = {}
    demographic_info: Dict[str, Any] = {}
    similar_faces: List[Dict[str, Any]] = []

class AdvancedSearchRequest(BaseModel):
    queries: List[str] = Field(..., min_items=1, max_items=10)
    search_types: List[SearchType] = [SearchType.TEXT]
    filters: Optional[SearchFilters] = None
    language: Optional[str] = "en"
    limit: Optional[int] = Field(50, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0)
    include_related: Optional[bool] = True
    sort_by: Optional[str] = "relevance"  # relevance, date, confidence, risk
    sort_order: Optional[str] = "desc"  # asc, desc

class AdvancedSearchResponse(BaseModel):
    queries: List[str]
    results: Dict[str, List[SearchResult]]  # search_type -> results
    total_counts: Dict[str, int]
    execution_time: float
    related_searches: List[str] = []
    insights: Dict[str, Any] = {}

class SearchSuggestion(BaseModel):
    query: str
    type: str  # autocomplete, related, trending
    confidence: float = Field(..., ge=0.0, le=1.0)
    metadata: Dict[str, Any] = {}

class SearchHistory(BaseModel):
    id: str
    query: str
    search_type: SearchType
    results_count: int
    execution_time: float
    created_at: datetime
    filters: Optional[SearchFilters] = None

class SearchAnalytics(BaseModel):
    total_searches: int
    searches_by_type: Dict[str, int]
    average_execution_time: float
    most_common_queries: List[Dict[str, Any]]
    search_success_rate: float
    popular_filters: Dict[str, Any]
    time_period: Dict[str, datetime] 