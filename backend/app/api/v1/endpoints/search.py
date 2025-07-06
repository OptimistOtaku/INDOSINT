from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
import structlog

from app.core.database import get_db, get_elasticsearch_client
from app.core.security import get_current_user, require_viewer
from app.models.user import User
from app.schemas.search import (
    SearchRequest, SearchResponse, SearchResult, 
    VoiceSearchRequest, ImageSearchRequest, FaceSearchRequest
)
from app.services.search_service import SearchService
from app.services.nlp_service import NLPService
from app.services.face_recognition_service import FaceRecognitionService

router = APIRouter()
logger = structlog.get_logger()

@router.post("/text", response_model=SearchResponse)
async def text_search(
    search_request: SearchRequest,
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Perform text-based OSINT search
    """
    try:
        search_service = SearchService(db, get_elasticsearch_client())
        results = await search_service.text_search(
            query=search_request.query,
            filters=search_request.filters,
            language=search_request.language or current_user.language_preference,
            limit=search_request.limit or 50,
            offset=search_request.offset or 0
        )
        
        logger.info(
            "Text search performed",
            user_id=current_user.id,
            query=search_request.query,
            results_count=len(results)
        )
        
        return SearchResponse(
            query=search_request.query,
            results=results,
            total_count=len(results),
            search_type="text"
        )
        
    except Exception as e:
        logger.error("Text search failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Search failed"
        )

@router.post("/voice", response_model=SearchResponse)
async def voice_search(
    search_request: VoiceSearchRequest,
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Perform voice-based OSINT search
    """
    try:
        nlp_service = NLPService()
        search_service = SearchService(db, get_elasticsearch_client())
        
        # Convert voice to text
        text_query = await nlp_service.speech_to_text(
            audio_data=search_request.audio_data,
            language=search_request.language or current_user.language_preference
        )
        
        # Perform text search
        results = await search_service.text_search(
            query=text_query,
            filters=search_request.filters,
            language=search_request.language or current_user.language_preference,
            limit=search_request.limit or 50,
            offset=search_request.offset or 0
        )
        
        logger.info(
            "Voice search performed",
            user_id=current_user.id,
            original_query=text_query,
            results_count=len(results)
        )
        
        return SearchResponse(
            query=text_query,
            results=results,
            total_count=len(results),
            search_type="voice"
        )
        
    except Exception as e:
        logger.error("Voice search failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Voice search failed"
        )

@router.post("/image", response_model=SearchResponse)
async def image_search(
    search_request: ImageSearchRequest,
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Perform image-based OSINT search
    """
    try:
        search_service = SearchService(db, get_elasticsearch_client())
        results = await search_service.image_search(
            image_data=search_request.image_data,
            search_type=search_request.search_type,  # object, text, scene
            filters=search_request.filters,
            limit=search_request.limit or 50,
            offset=search_request.offset or 0
        )
        
        logger.info(
            "Image search performed",
            user_id=current_user.id,
            search_type=search_request.search_type,
            results_count=len(results)
        )
        
        return SearchResponse(
            query=f"Image search: {search_request.search_type}",
            results=results,
            total_count=len(results),
            search_type="image"
        )
        
    except Exception as e:
        logger.error("Image search failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Image search failed"
        )

@router.post("/face", response_model=SearchResponse)
async def face_search(
    search_request: FaceSearchRequest,
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Perform face recognition search
    """
    try:
        face_service = FaceRecognitionService()
        search_service = SearchService(db, get_elasticsearch_client())
        
        # Extract face features
        face_features = await face_service.extract_face_features(
            image_data=search_request.image_data
        )
        
        # Search for similar faces
        results = await search_service.face_search(
            face_features=face_features,
            confidence_threshold=search_request.confidence_threshold or 0.8,
            filters=search_request.filters,
            limit=search_request.limit or 20,
            offset=search_request.offset or 0
        )
        
        logger.info(
            "Face search performed",
            user_id=current_user.id,
            confidence_threshold=search_request.confidence_threshold,
            results_count=len(results)
        )
        
        return SearchResponse(
            query="Face recognition search",
            results=results,
            total_count=len(results),
            search_type="face"
        )
        
    except Exception as e:
        logger.error("Face search failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Face search failed"
        )

@router.post("/upload-face", response_model=SearchResponse)
async def upload_face_search(
    file: UploadFile = File(...),
    confidence_threshold: float = Query(0.8, ge=0.0, le=1.0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Upload face image and perform search
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read file content
        image_data = await file.read()
        
        face_service = FaceRecognitionService()
        search_service = SearchService(db, get_elasticsearch_client())
        
        # Extract face features
        face_features = await face_service.extract_face_features(image_data)
        
        # Search for similar faces
        results = await search_service.face_search(
            face_features=face_features,
            confidence_threshold=confidence_threshold,
            limit=limit
        )
        
        logger.info(
            "Face upload search performed",
            user_id=current_user.id,
            filename=file.filename,
            results_count=len(results)
        )
        
        return SearchResponse(
            query=f"Face search: {file.filename}",
            results=results,
            total_count=len(results),
            search_type="face_upload"
        )
        
    except Exception as e:
        logger.error("Face upload search failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Face search failed"
        )

@router.get("/suggestions")
async def get_search_suggestions(
    query: str = Query(..., min_length=1),
    language: str = Query("en"),
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get search suggestions based on query
    """
    try:
        nlp_service = NLPService()
        suggestions = await nlp_service.get_search_suggestions(
            query=query,
            language=language or current_user.language_preference
        )
        
        return {
            "query": query,
            "suggestions": suggestions
        }
        
    except Exception as e:
        logger.error("Search suggestions failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get suggestions"
        )

@router.get("/trending")
async def get_trending_searches(
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get trending search terms
    """
    try:
        search_service = SearchService(db, get_elasticsearch_client())
        trending = await search_service.get_trending_searches()
        
        return {
            "trending_searches": trending
        }
        
    except Exception as e:
        logger.error("Trending searches failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get trending searches"
        )

@router.get("/history")
async def get_search_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get user's search history
    """
    try:
        search_service = SearchService(db, get_elasticsearch_client())
        history = await search_service.get_search_history(
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )
        
        return {
            "search_history": history,
            "total_count": len(history)
        }
        
    except Exception as e:
        logger.error("Search history failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get search history"
        )

@router.delete("/history")
async def clear_search_history(
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> Any:
    """
    Clear user's search history
    """
    try:
        search_service = SearchService(db, get_elasticsearch_client())
        await search_service.clear_search_history(user_id=current_user.id)
        
        logger.info("Search history cleared", user_id=current_user.id)
        
        return {"message": "Search history cleared successfully"}
        
    except Exception as e:
        logger.error("Clear search history failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear search history"
        ) 