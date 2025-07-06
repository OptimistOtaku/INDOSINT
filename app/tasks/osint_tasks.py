from celery import shared_task
from app import db
from app.models import SearchHistory, OSINTData, User
from app.services.social_media import SocialMediaService
from app.services.digital_footprint import DigitalFootprintService
from app.services.face_recognition import FaceRecognitionService
from app.services.nlp import NLPService
from app.services.translation import TranslationService
from datetime import datetime, timedelta
import time
import random

# Initialize services
social_media_service = SocialMediaService()
digital_footprint_service = DigitalFootprintService()
face_recognition_service = FaceRecognitionService()
nlp_service = NLPService()
translation_service = TranslationService()

@shared_task
def comprehensive_search_task(search_id: str, query: str, search_type: str, filters: dict, user_id: str):
    """
    Comprehensive OSINT search task
    
    Args:
        search_id: ID of the search history record
        query: Search query
        search_type: Type of search to perform
        filters: Search filters
        user_id: User ID who initiated the search
    """
    try:
        # Update search status to processing
        search_history = SearchHistory.query.get(search_id)
        if not search_history:
            return {'error': 'Search history not found'}
        
        search_history.status = 'processing'
        db.session.commit()
        
        start_time = time.time()
        results = []
        
        # Perform search based on type
        if search_type in ['social_media', 'comprehensive']:
            # Social media search
            social_results = social_media_service.search(query, 'en', filters)
            results.extend(social_results)
        
        if search_type in ['digital_footprint', 'comprehensive']:
            # Digital footprint search
            footprint_results = digital_footprint_service.search(query, filters)
            results.extend(footprint_results)
        
        if search_type in ['face_recognition', 'comprehensive'] and filters.get('image_url'):
            # Face recognition search
            face_results = face_recognition_service.search(query, filters['image_url'], filters)
            results.extend(face_results)
        
        # Save results to database
        for result in results:
            osint_data = OSINTData(
                user_id=user_id,
                search_query=query,
                data_type=result['type'],
                source=result['source'],
                content=result['content'],
                confidence_score=result.get('confidence_score', 0.0),
                language=result.get('language', 'en'),
                location=result.get('location'),
                timestamp=datetime.utcnow(),
                tags=result.get('tags', [])
            )
            db.session.add(osint_data)
        
        # Update search history
        execution_time = time.time() - start_time
        search_history.results_count = len(results)
        search_history.execution_time = execution_time
        search_history.status = 'completed'
        
        db.session.commit()
        
        return {
            'search_id': search_id,
            'status': 'completed',
            'results_count': len(results),
            'execution_time': execution_time
        }
        
    except Exception as e:
        # Update search status to failed
        if search_history:
            search_history.status = 'failed'
            db.session.commit()
        
        return {
            'search_id': search_id,
            'status': 'failed',
            'error': str(e)
        }

@shared_task
def social_media_search_task(search_id: str, query: str, platforms: list, language: str, filters: dict, user_id: str):
    """
    Social media search task
    
    Args:
        search_id: ID of the search history record
        query: Search query
        platforms: List of platforms to search
        language: Language preference
        filters: Search filters
        user_id: User ID who initiated the search
    """
    try:
        # Update search status
        search_history = SearchHistory.query.get(search_id)
        if not search_history:
            return {'error': 'Search history not found'}
        
        search_history.status = 'processing'
        db.session.commit()
        
        start_time = time.time()
        
        # Perform social media search
        results = social_media_service.search(query, language, filters, platforms)
        
        # Save results to database
        for result in results:
            osint_data = OSINTData(
                user_id=user_id,
                search_query=query,
                data_type='social_media',
                source=result['source'],
                content=result['content'],
                confidence_score=result.get('confidence_score', 0.0),
                language=result.get('language', language),
                location=result.get('location'),
                timestamp=datetime.utcnow(),
                tags=result.get('tags', [])
            )
            db.session.add(osint_data)
        
        # Update search history
        execution_time = time.time() - start_time
        search_history.results_count = len(results)
        search_history.execution_time = execution_time
        search_history.status = 'completed'
        
        db.session.commit()
        
        return {
            'search_id': search_id,
            'status': 'completed',
            'results_count': len(results),
            'execution_time': execution_time
        }
        
    except Exception as e:
        if search_history:
            search_history.status = 'failed'
            db.session.commit()
        
        return {
            'search_id': search_id,
            'status': 'failed',
            'error': str(e)
        }

@shared_task
def digital_footprint_search_task(search_id: str, query: str, search_types: list, filters: dict, user_id: str):
    """
    Digital footprint search task
    
    Args:
        search_id: ID of the search history record
        query: Search query
        search_types: Types of search to perform
        filters: Search filters
        user_id: User ID who initiated the search
    """
    try:
        # Update search status
        search_history = SearchHistory.query.get(search_id)
        if not search_history:
            return {'error': 'Search history not found'}
        
        search_history.status = 'processing'
        db.session.commit()
        
        start_time = time.time()
        
        # Perform digital footprint search
        results = digital_footprint_service.search(query, filters, search_types)
        
        # Save results to database
        for result in results:
            osint_data = OSINTData(
                user_id=user_id,
                search_query=query,
                data_type='digital_footprint',
                source=result['source'],
                content=result['content'],
                confidence_score=result.get('confidence_score', 0.0),
                timestamp=datetime.utcnow(),
                tags=result.get('tags', [])
            )
            db.session.add(osint_data)
        
        # Update search history
        execution_time = time.time() - start_time
        search_history.results_count = len(results)
        search_history.execution_time = execution_time
        search_history.status = 'completed'
        
        db.session.commit()
        
        return {
            'search_id': search_id,
            'status': 'completed',
            'results_count': len(results),
            'execution_time': execution_time
        }
        
    except Exception as e:
        if search_history:
            search_history.status = 'failed'
            db.session.commit()
        
        return {
            'search_id': search_id,
            'status': 'failed',
            'error': str(e)
        }

@shared_task
def face_recognition_search_task(search_id: str, query: str, image_url: str, filters: dict, user_id: str):
    """
    Face recognition search task
    
    Args:
        search_id: ID of the search history record
        query: Search query
        image_url: URL of the image to search for
        filters: Search filters
        user_id: User ID who initiated the search
    """
    try:
        # Update search status
        search_history = SearchHistory.query.get(search_id)
        if not search_history:
            return {'error': 'Search history not found'}
        
        search_history.status = 'processing'
        db.session.commit()
        
        start_time = time.time()
        
        # Perform face recognition search
        results = face_recognition_service.search(query, image_url, filters)
        
        # Save results to database
        for result in results:
            osint_data = OSINTData(
                user_id=user_id,
                search_query=query,
                data_type='face_recognition',
                source=result['source'],
                content=result['content'],
                confidence_score=result.get('confidence_score', 0.0),
                timestamp=datetime.utcnow(),
                tags=result.get('tags', [])
            )
            db.session.add(osint_data)
        
        # Update search history
        execution_time = time.time() - start_time
        search_history.results_count = len(results)
        search_history.execution_time = execution_time
        search_history.status = 'completed'
        
        db.session.commit()
        
        return {
            'search_id': search_id,
            'status': 'completed',
            'results_count': len(results),
            'execution_time': execution_time
        }
        
    except Exception as e:
        if search_history:
            search_history.status = 'failed'
            db.session.commit()
        
        return {
            'search_id': search_id,
            'status': 'failed',
            'error': str(e)
        }

@shared_task
def nlp_analysis_task(text: str, analysis_type: str, user_id: str):
    """
    NLP analysis task
    
    Args:
        text: Text to analyze
        analysis_type: Type of analysis (sentiment, entities, keywords, language)
        user_id: User ID who initiated the analysis
    """
    try:
        start_time = time.time()
        
        # Perform NLP analysis
        if analysis_type == 'sentiment':
            result = nlp_service.analyze_sentiment(text)
        elif analysis_type == 'entities':
            result = nlp_service.extract_entities(text)
        elif analysis_type == 'keywords':
            result = nlp_service.extract_keywords(text)
        elif analysis_type == 'language':
            result = nlp_service.detect_language(text)
        else:
            return {'error': 'Invalid analysis type'}
        
        execution_time = time.time() - start_time
        
        return {
            'analysis_type': analysis_type,
            'text': text,
            'result': result,
            'execution_time': execution_time
        }
        
    except Exception as e:
        return {
            'analysis_type': analysis_type,
            'status': 'failed',
            'error': str(e)
        }

@shared_task
def translation_task(text: str, source_language: str, target_language: str, user_id: str):
    """
    Translation task
    
    Args:
        text: Text to translate
        source_language: Source language code
        target_language: Target language code
        user_id: User ID who initiated the translation
    """
    try:
        start_time = time.time()
        
        # Perform translation
        translated_text = translation_service.translate(text, source_language, target_language)
        
        execution_time = time.time() - start_time
        
        return {
            'original_text': text,
            'translated_text': translated_text,
            'source_language': source_language,
            'target_language': target_language,
            'execution_time': execution_time
        }
        
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

@shared_task
def batch_translation_task(texts: list, source_language: str, target_language: str, user_id: str):
    """
    Batch translation task
    
    Args:
        texts: List of texts to translate
        source_language: Source language code
        target_language: Target language code
        user_id: User ID who initiated the translation
    """
    try:
        start_time = time.time()
        
        # Perform batch translation
        translated_texts = translation_service.translate_batch(texts, source_language, target_language)
        
        execution_time = time.time() - start_time
        
        return {
            'original_texts': texts,
            'translated_texts': translated_texts,
            'source_language': source_language,
            'target_language': target_language,
            'execution_time': execution_time
        }
        
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

@shared_task
def data_cleanup_task():
    """
    Clean up old data and optimize database
    """
    try:
        # Clean up old search history (older than 90 days)
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        old_searches = SearchHistory.query.filter(SearchHistory.created_at < cutoff_date).all()
        
        for search in old_searches:
            db.session.delete(search)
        
        # Clean up old OSINT data (older than 180 days)
        cutoff_date = datetime.utcnow() - timedelta(days=180)
        old_data = OSINTData.query.filter(OSINTData.created_at < cutoff_date).all()
        
        for data in old_data:
            db.session.delete(data)
        
        db.session.commit()
        
        return {
            'status': 'completed',
            'searches_deleted': len(old_searches),
            'data_deleted': len(old_data)
        }
        
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

@shared_task
def analytics_generation_task(user_id: str, analytics_type: str, period: str = 'daily'):
    """
    Generate analytics data for a user
    
    Args:
        user_id: User ID
        analytics_type: Type of analytics to generate
        period: Time period for analytics
    """
    try:
        from app.models import Analytics
        
        # Calculate date range
        end_date = datetime.utcnow()
        if period == 'daily':
            start_date = end_date - timedelta(days=30)
        elif period == 'weekly':
            start_date = end_date - timedelta(weeks=12)
        elif period == 'monthly':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Generate analytics data based on type
        if analytics_type == 'search_trends':
            data = _generate_search_trends(user_id, start_date, end_date)
        elif analytics_type == 'user_activity':
            data = _generate_user_activity(user_id, start_date, end_date)
        elif analytics_type == 'data_insights':
            data = _generate_data_insights(user_id, start_date, end_date)
        else:
            return {'error': 'Invalid analytics type'}
        
        # Save analytics data
        analytics = Analytics(
            user_id=user_id,
            analytics_type=analytics_type,
            data=data,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(analytics)
        db.session.commit()
        
        return {
            'status': 'completed',
            'analytics_type': analytics_type,
            'period': period,
            'data_points': len(data) if isinstance(data, list) else 1
        }
        
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

def _generate_search_trends(user_id: str, start_date: datetime, end_date: datetime) -> dict:
    """Generate search trends analytics"""
    # Mock search trends data
    return {
        'total_searches': random.randint(50, 200),
        'searches_by_type': {
            'social_media': random.randint(20, 80),
            'digital_footprint': random.randint(10, 40),
            'face_recognition': random.randint(5, 20),
            'comprehensive': random.randint(15, 60)
        },
        'daily_trend': [
            {
                'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                'searches': random.randint(1, 10),
                'results': random.randint(5, 50)
            }
            for i in range((end_date - start_date).days)
        ]
    }

def _generate_user_activity(user_id: str, start_date: datetime, end_date: datetime) -> dict:
    """Generate user activity analytics"""
    # Mock user activity data
    return {
        'active_days': random.randint(15, 30),
        'avg_searches_per_day': round(random.uniform(2.0, 8.0), 2),
        'peak_activity_hours': [9, 14, 20],
        'most_used_features': [
            'social_media_search',
            'digital_footprint',
            'face_recognition',
            'translation'
        ],
        'session_duration': round(random.uniform(10.0, 45.0), 2)
    }

def _generate_data_insights(user_id: str, start_date: datetime, end_date: datetime) -> dict:
    """Generate data insights analytics"""
    # Mock data insights
    return {
        'total_results': random.randint(200, 1000),
        'results_by_source': {
            'twitter': random.randint(50, 200),
            'linkedin': random.randint(30, 150),
            'facebook': random.randint(40, 180),
            'instagram': random.randint(25, 120),
            'data_breaches': random.randint(10, 50)
        },
        'confidence_distribution': {
            'high': random.randint(30, 60),
            'medium': random.randint(20, 40),
            'low': random.randint(10, 30)
        },
        'top_locations': [
            'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'
        ]
    } 