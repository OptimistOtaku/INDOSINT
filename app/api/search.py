from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, OSINTData, SearchHistory
from sqlalchemy import or_, and_
from datetime import datetime, timedelta

search_bp = Blueprint('search', __name__)

@search_bp.route('/advanced', methods=['POST'])
@jwt_required()
def advanced_search():
    """Advanced search with multiple filters"""
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    
    if not data.get('query'):
        return jsonify({'error': 'Search query is required'}), 400
    
    # Build query
    query = OSINTData.query.filter_by(user_id=current_user_id)
    
    # Text search
    search_query = data['query']
    query = query.filter(
        or_(
            OSINTData.search_query.contains(search_query),
            OSINTData.content.contains(search_query)
        )
    )
    
    # Data type filter
    if data.get('data_types'):
        query = query.filter(OSINTData.data_type.in_(data['data_types']))
    
    # Source filter
    if data.get('sources'):
        query = query.filter(OSINTData.source.in_(data['sources']))
    
    # Date range filter
    if data.get('date_from'):
        try:
            date_from = datetime.fromisoformat(data['date_from'])
            query = query.filter(OSINTData.timestamp >= date_from)
        except ValueError:
            return jsonify({'error': 'Invalid date_from format'}), 400
    
    if data.get('date_to'):
        try:
            date_to = datetime.fromisoformat(data['date_to'])
            query = query.filter(OSINTData.timestamp <= date_to)
        except ValueError:
            return jsonify({'error': 'Invalid date_to format'}), 400
    
    # Language filter
    if data.get('languages'):
        query = query.filter(OSINTData.language.in_(data['languages']))
    
    # Location filter
    if data.get('locations'):
        query = query.filter(OSINTData.location.in_(data['locations']))
    
    # Confidence score filter
    if data.get('min_confidence'):
        query = query.filter(OSINTData.confidence_score >= data['min_confidence'])
    
    if data.get('max_confidence'):
        query = query.filter(OSINTData.confidence_score <= data['max_confidence'])
    
    # Tags filter
    if data.get('tags'):
        for tag in data['tags']:
            query = query.filter(OSINTData.tags.contains([tag]))
    
    # Verification filter
    if data.get('verified_only'):
        query = query.filter(OSINTData.is_verified == True)
    
    # Pagination
    page = data.get('page', 1)
    per_page = data.get('per_page', 20)
    
    # Sorting
    sort_by = data.get('sort_by', 'timestamp')
    sort_order = data.get('sort_order', 'desc')
    
    if sort_order == 'desc':
        query = query.order_by(getattr(OSINTData, sort_by).desc())
    else:
        query = query.order_by(getattr(OSINTData, sort_by).asc())
    
    # Execute query
    results = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'results': [result.to_dict() for result in results.items],
        'total': results.total,
        'pages': results.pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': results.has_next,
        'has_prev': results.has_prev
    }), 200

@search_bp.route('/saved', methods=['GET'])
@jwt_required()
def get_saved_searches():
    """Get user's saved searches"""
    current_user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Get search history with saved flag
    saved_searches = SearchHistory.query.filter_by(
        user_id=current_user_id
    ).order_by(SearchHistory.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'saved_searches': [search.to_dict() for search in saved_searches.items],
        'total': saved_searches.total,
        'pages': saved_searches.pages,
        'current_page': page,
        'per_page': per_page
    }), 200

@search_bp.route('/suggestions', methods=['GET'])
@jwt_required()
def get_search_suggestions():
    """Get search suggestions based on user history"""
    current_user_id = get_jwt_identity()
    
    query = request.args.get('q', '')
    if not query:
        return jsonify({'suggestions': []}), 200
    
    # Get recent searches containing the query
    recent_searches = SearchHistory.query.filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.query.contains(query)
    ).order_by(SearchHistory.created_at.desc()).limit(10).all()
    
    # Get popular search terms
    popular_searches = db.session.query(
        SearchHistory.query,
        db.func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.query.contains(query)
    ).group_by(SearchHistory.query).order_by(
        db.func.count(SearchHistory.id).desc()
    ).limit(10).all()
    
    suggestions = []
    
    # Add recent searches
    for search in recent_searches:
        suggestions.append({
            'type': 'recent',
            'query': search.query,
            'search_type': search.search_type,
            'created_at': search.created_at.isoformat()
        })
    
    # Add popular searches
    for search, count in popular_searches:
        suggestions.append({
            'type': 'popular',
            'query': search,
            'count': count
        })
    
    return jsonify({'suggestions': suggestions}), 200

@search_bp.route('/export', methods=['POST'])
@jwt_required()
def export_search_results():
    """Export search results in various formats"""
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    
    if not data.get('search_ids'):
        return jsonify({'error': 'Search IDs are required'}), 400
    
    export_format = data.get('format', 'json')  # json, csv, pdf
    include_metadata = data.get('include_metadata', True)
    
    try:
        # Get search results
        search_results = []
        for search_id in data['search_ids']:
            search_history = SearchHistory.query.filter_by(
                id=search_id, user_id=current_user_id
            ).first()
            
            if search_history:
                osint_data = OSINTData.query.filter_by(
                    user_id=current_user_id,
                    search_query=search_history.query
                ).all()
                
                search_results.append({
                    'search': search_history.to_dict() if include_metadata else None,
                    'results': [data.to_dict() for data in osint_data]
                })
        
        # Generate export based on format
        if export_format == 'json':
            return jsonify({
                'export_data': search_results,
                'format': 'json',
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        elif export_format == 'csv':
            # TODO: Implement CSV export
            return jsonify({'error': 'CSV export not implemented yet'}), 501
        elif export_format == 'pdf':
            # TODO: Implement PDF export
            return jsonify({'error': 'PDF export not implemented yet'}), 501
        else:
            return jsonify({'error': 'Unsupported export format'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@search_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_search_analytics():
    """Get search analytics for the user"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Total searches
    total_searches = SearchHistory.query.filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).count()
    
    # Searches by type
    searches_by_type = db.session.query(
        SearchHistory.search_type,
        db.func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(SearchHistory.search_type).all()
    
    # Average execution time
    avg_execution_time = db.session.query(
        db.func.avg(SearchHistory.execution_time)
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from,
        SearchHistory.execution_time.isnot(None)
    ).scalar() or 0
    
    # Total results found
    total_results = db.session.query(
        db.func.sum(SearchHistory.results_count)
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).scalar() or 0
    
    # Daily search trend
    daily_trend = db.session.query(
        db.func.date(SearchHistory.created_at).label('date'),
        db.func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(
        db.func.date(SearchHistory.created_at)
    ).order_by(
        db.func.date(SearchHistory.created_at)
    ).all()
    
    return jsonify({
        'total_searches': total_searches,
        'searches_by_type': {search_type: count for search_type, count in searches_by_type},
        'avg_execution_time': float(avg_execution_time),
        'total_results': int(total_results),
        'daily_trend': [{'date': str(date), 'count': count} for date, count in daily_trend]
    }), 200 