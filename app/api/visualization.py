from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, OSINTData, SearchHistory
from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta
import json

viz_bp = Blueprint('visualization', __name__)

@viz_bp.route('/charts/search-activity', methods=['GET'])
@jwt_required()
def get_search_activity_chart():
    """Get search activity chart data"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Daily search activity
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
    
    # Format for chart
    chart_data = {
        'labels': [str(date) for date, _, _ in daily_activity],
        'datasets': [
            {
                'label': 'Searches',
                'data': [int(searches) for _, searches, _ in daily_activity],
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'tension': 0.1
            },
            {
                'label': 'Results',
                'data': [int(results) if results else 0 for _, _, results in daily_activity],
                'borderColor': 'rgb(255, 99, 132)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'tension': 0.1
            }
        ]
    }
    
    return jsonify(chart_data), 200

@viz_bp.route('/charts/search-types', methods=['GET'])
@jwt_required()
def get_search_types_chart():
    """Get search types distribution chart"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Search types distribution
    search_types = db.session.query(
        SearchHistory.search_type,
        func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(SearchHistory.search_type).all()
    
    # Colors for different search types
    colors = [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
        'rgb(255, 159, 64)'
    ]
    
    chart_data = {
        'labels': [search_type for search_type, _ in search_types],
        'datasets': [{
            'data': [count for _, count in search_types],
            'backgroundColor': colors[:len(search_types)],
            'borderWidth': 1
        }]
    }
    
    return jsonify(chart_data), 200

@viz_bp.route('/charts/data-sources', methods=['GET'])
@jwt_required()
def get_data_sources_chart():
    """Get data sources distribution chart"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Data sources distribution
    data_sources = db.session.query(
        OSINTData.source,
        func.count(OSINTData.id).label('count')
    ).filter(
        OSINTData.user_id == current_user_id,
        OSINTData.created_at >= date_from
    ).group_by(OSINTData.source).all()
    
    # Colors for different sources
    colors = [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
        'rgb(255, 159, 64)',
        'rgb(201, 203, 207)'
    ]
    
    chart_data = {
        'labels': [source for source, _ in data_sources],
        'datasets': [{
            'data': [count for _, count in data_sources],
            'backgroundColor': colors[:len(data_sources)],
            'borderWidth': 1
        }]
    }
    
    return jsonify(chart_data), 200

@viz_bp.route('/charts/performance', methods=['GET'])
@jwt_required()
def get_performance_chart():
    """Get performance metrics chart"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Performance by search type
    performance = db.session.query(
        SearchHistory.search_type,
        func.avg(SearchHistory.execution_time).label('avg_time'),
        func.count(SearchHistory.id).label('total_searches')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from,
        SearchHistory.execution_time.isnot(None)
    ).group_by(SearchHistory.search_type).all()
    
    chart_data = {
        'labels': [search_type for search_type, _, _ in performance],
        'datasets': [
            {
                'label': 'Average Execution Time (seconds)',
                'data': [float(avg_time) if avg_time else 0 for _, avg_time, _ in performance],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgb(75, 192, 192)',
                'borderWidth': 2
            },
            {
                'label': 'Total Searches',
                'data': [int(total) for _, _, total in performance],
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgb(255, 99, 132)',
                'borderWidth': 2,
                'yAxisID': 'y1'
            }
        ]
    }
    
    return jsonify(chart_data), 200

@viz_bp.route('/charts/confidence-distribution', methods=['GET'])
@jwt_required()
def get_confidence_distribution_chart():
    """Get confidence score distribution chart"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Confidence score ranges
    confidence_ranges = [
        (0.0, 0.2, 'Very Low'),
        (0.2, 0.4, 'Low'),
        (0.4, 0.6, 'Medium'),
        (0.6, 0.8, 'High'),
        (0.8, 1.0, 'Very High')
    ]
    
    distribution_data = []
    for min_score, max_score, label in confidence_ranges:
        count = db.session.query(func.count(OSINTData.id)).filter(
            OSINTData.user_id == current_user_id,
            OSINTData.created_at >= date_from,
            OSINTData.confidence_score >= min_score,
            OSINTData.confidence_score < max_score
        ).scalar()
        
        distribution_data.append({
            'range': label,
            'count': count
        })
    
    chart_data = {
        'labels': [item['range'] for item in distribution_data],
        'datasets': [{
            'label': 'Number of Results',
            'data': [item['count'] for item in distribution_data],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(153, 102, 255, 0.8)'
            ],
            'borderWidth': 1
        }]
    }
    
    return jsonify(chart_data), 200

@viz_bp.route('/charts/geographic', methods=['GET'])
@jwt_required()
def get_geographic_chart():
    """Get geographic distribution chart"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Geographic distribution
    locations = db.session.query(
        OSINTData.location,
        func.count(OSINTData.id).label('count')
    ).filter(
        OSINTData.user_id == current_user_id,
        OSINTData.created_at >= date_from,
        OSINTData.location.isnot(None)
    ).group_by(OSINTData.location).all()
    
    # Filter out empty locations and limit to top 10
    location_data = [
        {'location': location, 'count': count}
        for location, count in locations
        if location and location.strip()
    ][:10]
    
    chart_data = {
        'labels': [item['location'] for item in location_data],
        'datasets': [{
            'label': 'Results by Location',
            'data': [item['count'] for item in location_data],
            'backgroundColor': 'rgba(54, 162, 235, 0.8)',
            'borderColor': 'rgb(54, 162, 235)',
            'borderWidth': 1
        }]
    }
    
    return jsonify(chart_data), 200

@viz_bp.route('/charts/timeline', methods=['GET'])
@jwt_required()
def get_timeline_chart():
    """Get timeline visualization data"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Timeline data
    timeline_data = db.session.query(
        OSINTData.timestamp,
        OSINTData.data_type,
        OSINTData.source,
        OSINTData.confidence_score
    ).filter(
        OSINTData.user_id == current_user_id,
        OSINTData.created_at >= date_from
    ).order_by(OSINTData.timestamp).all()
    
    # Format for timeline
    timeline = []
    for timestamp, data_type, source, confidence in timeline_data:
        timeline.append({
            'timestamp': timestamp.isoformat(),
            'type': data_type,
            'source': source,
            'confidence': float(confidence) if confidence else 0,
            'title': f"{data_type.title()} from {source}",
            'description': f"Confidence: {confidence:.2f}" if confidence else "No confidence score"
        })
    
    return jsonify({
        'timeline': timeline,
        'total_events': len(timeline)
    }), 200

@viz_bp.route('/charts/heatmap', methods=['GET'])
@jwt_required()
def get_heatmap_data():
    """Get heatmap data for activity visualization"""
    current_user_id = get_jwt_identity()
    
    # Get date range
    days = request.args.get('days', 30, type=int)
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Activity by hour and day of week
    activity_data = db.session.query(
        func.extract('dow', SearchHistory.created_at).label('day_of_week'),
        func.extract('hour', SearchHistory.created_at).label('hour'),
        func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.user_id == current_user_id,
        SearchHistory.created_at >= date_from
    ).group_by(
        func.extract('dow', SearchHistory.created_at),
        func.extract('hour', SearchHistory.created_at)
    ).all()
    
    # Initialize heatmap data
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    hours = list(range(24))
    
    heatmap_data = []
    for day_of_week, hour, count in activity_data:
        heatmap_data.append({
            'day': days_of_week[int(day_of_week)],
            'hour': int(hour),
            'value': int(count)
        })
    
    return jsonify({
        'heatmap_data': heatmap_data,
        'days_of_week': days_of_week,
        'hours': hours
    }), 200

@viz_bp.route('/export-chart', methods=['POST'])
@jwt_required()
def export_chart():
    """Export chart data"""
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    
    if not data.get('chart_type'):
        return jsonify({'error': 'Chart type is required'}), 400
    
    chart_type = data['chart_type']
    format_type = data.get('format', 'json')
    
    try:
        # Get chart data based on type
        if chart_type == 'search_activity':
            chart_data = get_search_activity_chart_data(current_user_id)
        elif chart_type == 'search_types':
            chart_data = get_search_types_chart_data(current_user_id)
        elif chart_type == 'data_sources':
            chart_data = get_data_sources_chart_data(current_user_id)
        elif chart_type == 'performance':
            chart_data = get_performance_chart_data(current_user_id)
        else:
            return jsonify({'error': 'Invalid chart type'}), 400
        
        if format_type == 'json':
            return jsonify({
                'chart_type': chart_type,
                'data': chart_data,
                'exported_at': datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({'error': 'Unsupported export format'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

def get_search_activity_chart_data(user_id):
    """Helper function to get search activity chart data"""
    days = 30
    date_from = datetime.utcnow() - timedelta(days=days)
    
    daily_activity = db.session.query(
        func.date(SearchHistory.created_at).label('date'),
        func.count(SearchHistory.id).label('searches'),
        func.sum(SearchHistory.results_count).label('results')
    ).filter(
        SearchHistory.user_id == user_id,
        SearchHistory.created_at >= date_from
    ).group_by(
        func.date(SearchHistory.created_at)
    ).order_by(
        func.date(SearchHistory.created_at)
    ).all()
    
    return {
        'labels': [str(date) for date, _, _ in daily_activity],
        'datasets': [
            {
                'label': 'Searches',
                'data': [int(searches) for _, searches, _ in daily_activity]
            },
            {
                'label': 'Results',
                'data': [int(results) if results else 0 for _, _, results in daily_activity]
            }
        ]
    }

def get_search_types_chart_data(user_id):
    """Helper function to get search types chart data"""
    days = 30
    date_from = datetime.utcnow() - timedelta(days=days)
    
    search_types = db.session.query(
        SearchHistory.search_type,
        func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.user_id == user_id,
        SearchHistory.created_at >= date_from
    ).group_by(SearchHistory.search_type).all()
    
    return {
        'labels': [search_type for search_type, _ in search_types],
        'datasets': [{
            'data': [count for _, count in search_types]
        }]
    }

def get_data_sources_chart_data(user_id):
    """Helper function to get data sources chart data"""
    days = 30
    date_from = datetime.utcnow() - timedelta(days=days)
    
    data_sources = db.session.query(
        OSINTData.source,
        func.count(OSINTData.id).label('count')
    ).filter(
        OSINTData.user_id == user_id,
        OSINTData.created_at >= date_from
    ).group_by(OSINTData.source).all()
    
    return {
        'labels': [source for source, _ in data_sources],
        'datasets': [{
            'data': [count for _, count in data_sources]
        }]
    }

def get_performance_chart_data(user_id):
    """Helper function to get performance chart data"""
    days = 30
    date_from = datetime.utcnow() - timedelta(days=days)
    
    performance = db.session.query(
        SearchHistory.search_type,
        func.avg(SearchHistory.execution_time).label('avg_time'),
        func.count(SearchHistory.id).label('total_searches')
    ).filter(
        SearchHistory.user_id == user_id,
        SearchHistory.created_at >= date_from,
        SearchHistory.execution_time.isnot(None)
    ).group_by(SearchHistory.search_type).all()
    
    return {
        'labels': [search_type for search_type, _, _ in performance],
        'datasets': [
            {
                'label': 'Average Execution Time (seconds)',
                'data': [float(avg_time) if avg_time else 0 for _, avg_time, _ in performance]
            },
            {
                'label': 'Total Searches',
                'data': [int(total) for _, _, total in performance]
            }
        ]
    } 