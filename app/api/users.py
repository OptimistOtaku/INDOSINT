from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Organization, UserOrganization
from datetime import datetime

users_bp = Blueprint('users', __name__)

def admin_required(fn):
    """Decorator to check if user is admin"""
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@users_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Get all users (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    role = request.args.get('role', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.username.contains(search)) |
            (User.email.contains(search)) |
            (User.first_name.contains(search)) |
            (User.last_name.contains(search))
        )
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [user.to_dict() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page,
        'per_page': per_page
    }), 200

@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Users can only view their own profile unless they're admin
    if current_user_id != user_id and current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """Update user (admin only)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    allowed_fields = ['first_name', 'last_name', 'role', 'is_active', 'preferred_language', 'timezone']
    
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User update failed'}), 500

@users_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User deletion failed'}), 500

@users_bp.route('/<user_id>/organizations', methods=['GET'])
@jwt_required()
def get_user_organizations(user_id):
    """Get user's organizations"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Users can only view their own organizations unless they're admin
    if current_user_id != user_id and current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    user_orgs = UserOrganization.query.filter_by(user_id=user_id, is_active=True).all()
    
    organizations = []
    for user_org in user_orgs:
        org_data = user_org.organization.to_dict()
        org_data['user_role'] = user_org.role
        organizations.append(org_data)
    
    return jsonify({'organizations': organizations}), 200

@users_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_user_stats():
    """Get user statistics (admin only)"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    verified_users = User.query.filter_by(is_verified=True).count()
    
    # Users by role
    role_stats = db.session.query(User.role, db.func.count(User.id)).group_by(User.role).all()
    role_distribution = {role: count for role, count in role_stats}
    
    # Recent registrations
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'verified_users': verified_users,
        'role_distribution': role_distribution,
        'recent_users': [user.to_dict() for user in recent_users]
    }), 200 