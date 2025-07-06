from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, OSINTData, SearchHistory, Analytics
from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta
import json

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_analytics():
    """Get dashboard analytics for the user"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Total searches
    total_searches = SearchHistory.query.filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).count()
    
    # Total results found
    total_results = db.session.query(
        func.sum(SearchHistory.results_count)
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).scalar() or 0
    
    # Average execution time
    avg_execution_time = db.session.query(
        func.avg(SearchHistory.execution_time)
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from,
        SearchHistory.execution_time.isnot(None)
    ).scalar() or 0
    
    # Searches by type
    searches_by_type = db.session.query(
        SearchHistory.search_type,
        func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(SearchHistory.search_type).all()
    
    # Data by source
    data_by_source = db.session.query(
        OSINTData.source,
        func.count(OSINTData.id).label('count')
    ).filter(
        OSINTData.user_id == current_user_id,
        OSINTData.created_at >= date_from
    ).group_by(OSINTData.source).all()
    
    # Data by type
    data_by_type = db.session.query(
        OSINTData.data_type,
        func.count(OSINTData.id).label('count')
    ).filter(
        OSINTData.user_id == current_user_id,
        OSINTData.created_at >= date_from
    ).group_by(OSINTData.data_type).all()
    
    # Daily activity
    daily_activity = db.session.query(
        func.date(SearchHistory.created_at).label('date'),
        func.count(SearchHistory.id).label('searches'),
        func.sum(SearchHistory.results_count).label('results')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(
        func.date(SearchHistory.created_at)
    ).order_by(
        func.date(SearchHistory.created_at)
    ).all()
    
    # Top search queries
    top_queries = db.session.query(
        SearchHistory.query,
        func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(SearchHistory.query).order_by(
        func.count(SearchHistory.id).desc()
    ).limit(10).all()
    
    return jsonify({
        'overview': {
            'total_searches': total_searches,
            'total_results': int(total_results),
            'avg_execution_time': float(avg_execution_time),
            'success_rate': 95.5  # Mock data
        },
        'searches_by_type': {search_type: count for search_type, count in searches_by_type},
        'data_by_source': {source: count for source, count in data_by_source},
        'data_by_type': {data_type: count for data_type, count in data_by_type},
        'daily_activity': [
            {
                'date': str(date),
                'searches': int(searches),
                'results': int(results) if results else 0
            }
            for date, searches, results in daily_activity
        ],
        'top_queries': [{'query': query, 'count': count} for query, count in top_queries]
    }), 200

@analytics_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends():
    """Get trend analysis"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 90, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Weekly trends
    weekly_trends = db.session.query(
        func.date_trunc('week', SearchHistory.created_at).label('week'),
        func.count(SearchHistory.id).label('searches'),
        func.avg(SearchHistory.execution_time).label('avg_time'),
        func.sum(SearchHistory.results_count).label('total_results')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(
        func.date_trunc('week', SearchHistory.created_at)
    ).order_by(
        func.date_trunc('week', SearchHistory.created_at)
    ).all()
    
    # Search type trends
    type_trends = db.session.query(
        SearchHistory.search_type,
        func.date_trunc('week', SearchHistory.created_at).label('week'),
        func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(
        SearchHistory.search_type,
        func.date_trunc('week', SearchHistory.created_at)
    ).order_by(
        func.date_trunc('week', SearchHistory.created_at)
    ).all()
    
    # Process type trends
    type_trends_data = {}
    for search_type, week, count in type_trends:
        if search_type not in type_trends_data:
            type_trends_data[search_type] = []
        type_trends_data[search_type].append({
            'week': str(week),
            'count': count
        })
    
    return jsonify({
        'weekly_trends': [
            {
                'week': str(week),
                'searches': int(searches),
                'avg_time': float(avg_time) if avg_time else 0,
                'total_results': int(total_results) if total_results else 0
            }
            for week, searches, avg_time, total_results in weekly_trends
        ],
        'type_trends': type_trends_data
    }), 200

@analytics_bp.route('/insights', methods=['GET'])
@jwt_required()
def get_insights():
    """Get AI-powered insights"""
    current_user_id = get_jwt_identity()
    
    # Get recent data
    recent_data = OSINTData.query.filter_by(
        user_id=current_user_id
    ).order_by(OSINTData.created_at.desc()).limit(100).all()
    
    # Mock insights (in a real system, this would use ML models)
    insights = {
        'patterns': [
            {
                'type': 'search_pattern',
                'title': 'Most Active Search Times',
                'description': 'You are most active between 10 AM and 2 PM',
                'confidence': 0.85
            },
            {
                'type': 'data_pattern',
                'title': 'High Confidence Results',
                'description': '85% of your social media searches return high-confidence results',
                'confidence': 0.92
            }
        ],
        'recommendations': [
            {
                'type': 'optimization',
                'title': 'Optimize Search Queries',
                'description': 'Try using more specific keywords for better results',
                'priority': 'medium'
            },
            {
                'type': 'feature',
                'title': 'Enable Advanced Filters',
                'description': 'Use date range filters to narrow down results',
                'priority': 'low'
            }
        ],
        'anomalies': [
            {
                'type': 'performance',
                'title': 'Slow Search Performance',
                'description': 'Face recognition searches are taking longer than usual',
                'severity': 'medium',
                'timestamp': datetime.utcnow().isoformat()
            }
        ]
    }
    
    return jsonify(insights), 200

@analytics_bp.route('/performance', methods=['GET'])
@jwt_required()
def get_performance_metrics():
    """Get performance metrics"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Performance by search type
    performance_by_type = db.session.query(
        SearchHistory.search_type,
        func.avg(SearchHistory.execution_time).label('avg_time'),
        func.min(SearchHistory.execution_time).label('min_time'),
        func.max(SearchHistory.execution_time).label('max_time'),
        func.count(SearchHistory.id).label('total_searches')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from,
        SearchHistory.execution_time.isnot(None)
    ).group_by(SearchHistory.search_type).all()
    
    # Success rate by type
    success_by_type = db.session.query(
        SearchHistory.search_type,
        func.count(SearchHistory.id).label('total'),
        func.sum(
            func.case([(SearchHistory.status == 'completed', 1)], else_=0)
        ).label('successful')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(SearchHistory.search_type).all()
    
    # Results quality metrics
    quality_metrics = db.session.query(
        OSINTData.data_type,
        func.avg(OSINTData.confidence_score).label('avg_confidence'),
        func.count(OSINTData.id).label('total_results'),
        func.sum(
            func.case([(OSINTData.is_verified == True, 1)], else_=0)
        ).label('verified_results')
    ).filter(
        OSINTData.user_id == current_user_id,
        OSINTData.created_at >= date_from
    ).group_by(OSINTData.data_type).all()
    
    return jsonify({
        'performance_by_type': [
            {
                'search_type': search_type,
                'avg_time': float(avg_time) if avg_time else 0,
                'min_time': float(min_time) if min_time else 0,
                'max_time': float(max_time) if max_time else 0,
                'total_searches': int(total_searches)
            }
            for search_type, avg_time, min_time, max_time, total_searches in performance_by_type
        ],
        'success_by_type': [
            {
                'search_type': search_type,
                'total': int(total),
                'successful': int(successful),
                'success_rate': (float(successful) / float(total) * 100) if total > 0 else 0
            }
            for search_type, total, successful in success_by_type
        ],
        'quality_metrics': [
            {
                'data_type': data_type,
                'avg_confidence': float(avg_confidence) if avg_confidence else 0,
                'total_results': int(total_results),
                'verified_results': int(verified_results),
                'verification_rate': (float(verified_results) / float(total_results) * 100) if total_results > 0 else 0
            }
            for data_type, avg_confidence, total_results, verified_results in quality_metrics
        ]
    }), 200

@analytics_bp.route('/export', methods=['POST'])
@jwt_required()
def export_analytics():
    """Export analytics data"""
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    
    if not data.get('analytics_type'):
        return jsonify({'error': 'Analytics type is required'}), 400
    
    analytics_type = data['analytics_type']
    date_from = data.get('date_from')
    date_to = data.get('date_to')
    format_type = data.get('format', 'json')
    
    try:
        # Build query based on analytics type
        if analytics_type == 'search_history':
            query = SearchHistory.query.filter_by(user_id=current_user_id)
        elif analytics_type == 'osint_data':
            query = OSINTData.query.filter_by(user_id=current_user_id)
        else:
            return jsonify({'error': 'Invalid analytics type'}), 400
        
        # Apply date filters
        if date_from:
            query = query.filter(query.model.created_at >= date_from)
        if date_to:
            query = query.filter(query.model.created_at <= date_to)
        
        # Get data
        results = query.all()
        
        # Format for export
        export_data = [item.to_dict() for item in results]
        
        if format_type == 'json':
            return jsonify({
                'analytics_type': analytics_type,
                'total_records': len(export_data),
                'data': export_data,
                'exported_at': datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({'error': 'Unsupported export format'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500 