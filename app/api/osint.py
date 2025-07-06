from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, celery
from app.models import User, OSINTData, SearchHistory
from app.services.social_media import SocialMediaService
from app.services.digital_footprint import DigitalFootprintService
from app.services.face_recognition import FaceRecognitionService
from app.services.nlp import NLPService
from app.services.translation import TranslationService
from datetime import datetime
import time

osint_bp = Blueprint('osint', __name__)

# Initialize services
social_media_service = SocialMediaService()
digital_footprint_service = DigitalFootprintService()
face_recognition_service = FaceRecognitionService()
nlp_service = NLPService()
translation_service = TranslationService()

@osint_bp.route('/search', methods=['POST'])
@jwt_required()
def search():
    """Perform comprehensive OSINT search"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    data = request.get_json()
    
    if not data.get('query'):
        return jsonify({'error': 'Search query is required'}), 400
    
    search_type = data.get('type', 'comprehensive')  # social_media, digital_footprint, face_recognition, comprehensive
    language = data.get('language', user.preferred_language)
    filters = data.get('filters', {})
    
    # Record search start time
    start_time = time.time()
    
    try:
        # Create search history record
        search_history = SearchHistory(
            user_id=current_user_id,
            query=data['query'],
            search_type=search_type,
            filters=filters,
            status='pending'
        )
        db.session.add(search_history)
        db.session.commit()
        
        # Perform search based on type
        results = []
        
        if search_type in ['social_media', 'comprehensive']:
            # Social media search
            social_results = social_media_service.search(data['query'], language, filters)
            results.extend(social_results)
        
        if search_type in ['digital_footprint', 'comprehensive']:
            # Digital footprint search
            footprint_results = digital_footprint_service.search(data['query'], filters)
            results.extend(footprint_results)
        
        if search_type in ['face_recognition', 'comprehensive'] and data.get('image_url'):
            # Face recognition search
            face_results = face_recognition_service.search(data['query'], data['image_url'], filters)
            results.extend(face_results)
        
        # Save results to database
        for result in results:
            osint_data = OSINTData(
                user_id=current_user_id,
                search_query=data['query'],
                data_type=result['type'],
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
        
        return jsonify({
            'message': 'Search completed successfully',
            'results': results,
            'total_results': len(results),
            'execution_time': execution_time,
            'search_id': search_history.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@osint_bp.route('/social-media', methods=['POST'])
@jwt_required()
def social_media_search():
    """Search social media platforms"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    data = request.get_json()
    
    if not data.get('query'):
        return jsonify({'error': 'Search query is required'}), 400
    
    platforms = data.get('platforms', ['twitter', 'linkedin', 'facebook', 'instagram'])
    language = data.get('language', user.preferred_language)
    filters = data.get('filters', {})
    
    try:
        results = social_media_service.search(data['query'], language, filters, platforms)
        
        # Save to database
        for result in results:
            osint_data = OSINTData(
                user_id=current_user_id,
                search_query=data['query'],
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
        
        db.session.commit()
        
        return jsonify({
            'message': 'Social media search completed',
            'results': results,
            'total_results': len(results)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Social media search failed: {str(e)}'}), 500

@osint_bp.route('/digital-footprint', methods=['POST'])
@jwt_required()
def digital_footprint_search():
    """Search digital footprint"""
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    
    if not data.get('query'):
        return jsonify({'error': 'Search query is required'}), 400
    
    search_types = data.get('types', ['email_breaches', 'domain_registrations', 'data_breaches'])
    filters = data.get('filters', {})
    
    try:
        results = digital_footprint_service.search(data['query'], filters, search_types)
        
        # Save to database
        for result in results:
            osint_data = OSINTData(
                user_id=current_user_id,
                search_query=data['query'],
                data_type='digital_footprint',
                source=result['source'],
                content=result['content'],
                confidence_score=result.get('confidence_score', 0.0),
                timestamp=datetime.utcnow(),
                tags=result.get('tags', [])
            )
            db.session.add(osint_data)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Digital footprint search completed',
            'results': results,
            'total_results': len(results)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Digital footprint search failed: {str(e)}'}), 500

@osint_bp.route('/face-recognition', methods=['POST'])
@jwt_required()
def face_recognition_search():
    """Search using face recognition"""
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    
    if not data.get('query') or not data.get('image_url'):
        return jsonify({'error': 'Search query and image URL are required'}), 400
    
    filters = data.get('filters', {})
    
    try:
        results = face_recognition_service.search(data['query'], data['image_url'], filters)
        
        # Save to database
        for result in results:
            osint_data = OSINTData(
                user_id=current_user_id,
                search_query=data['query'],
                data_type='face_recognition',
                source=result['source'],
                content=result['content'],
                confidence_score=result.get('confidence_score', 0.0),
                timestamp=datetime.utcnow(),
                tags=result.get('tags', [])
            )
            db.session.add(osint_data)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Face recognition search completed',
            'results': results,
            'total_results': len(results)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Face recognition search failed: {str(e)}'}), 500

@osint_bp.route('/translate', methods=['POST'])
@jwt_required()
def translate_text():
    """Translate text between languages"""
    data = request.get_json()
    
    if not data.get('text') or not data.get('target_language'):
        return jsonify({'error': 'Text and target language are required'}), 400
    
    source_language = data.get('source_language', 'auto')
    
    try:
        translated_text = translation_service.translate(
            data['text'], 
            source_language, 
            data['target_language']
        )
        
        return jsonify({
            'original_text': data['text'],
            'translated_text': translated_text,
            'source_language': source_language,
            'target_language': data['target_language']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

@osint_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_text():
    """Analyze text using NLP"""
    data = request.get_json()
    
    if not data.get('text'):
        return jsonify({'error': 'Text is required'}), 400
    
    analysis_type = data.get('type', 'sentiment')  # sentiment, entities, keywords, language
    
    try:
        if analysis_type == 'sentiment':
            result = nlp_service.analyze_sentiment(data['text'])
        elif analysis_type == 'entities':
            result = nlp_service.extract_entities(data['text'])
        elif analysis_type == 'keywords':
            result = nlp_service.extract_keywords(data['text'])
        elif analysis_type == 'language':
            result = nlp_service.detect_language(data['text'])
        else:
            return jsonify({'error': 'Invalid analysis type'}), 400
        
        return jsonify({
            'text': data['text'],
            'analysis_type': analysis_type,
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@osint_bp.route('/history', methods=['GET'])
@jwt_required()
def get_search_history():
    """Get user's search history"""
    current_user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search_type = request.args.get('type', '')
    
    query = SearchHistory.query.filter_by(user_id=current_user_id)
    
    if search_type:
        query = query.filter(SearchHistory.search_type == search_type)
    
    history = query.order_by(SearchHistory.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'history': [item.to_dict() for item in history.items],
        'total': history.total,
        'pages': history.pages,
        'current_page': page,
        'per_page': per_page
    }), 200

@osint_bp.route('/results/<search_id>', methods=['GET'])
@jwt_required()
def get_search_results(search_id):
    """Get results for a specific search"""
    current_user_id = get_jwt_identity()
    
    # Verify search belongs to user
    search_history = SearchHistory.query.filter_by(
        id=search_id, user_id=current_user_id
    ).first()
    
    if not search_history:
        return jsonify({'error': 'Search not found'}), 404
    
    # Get OSINT data for this search
    osint_data = OSINTData.query.filter_by(
        user_id=current_user_id,
        search_query=search_history.query
    ).all()
    
    return jsonify({
        'search': search_history.to_dict(),
        'results': [data.to_dict() for data in osint_data]
    }), 200 