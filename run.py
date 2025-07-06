#!/usr/bin/env python3
"""
INDOSINT - AI-Powered OSINT System for India
Main application runner
"""

import os
import sys
from app import create_app, db
from app.models import User, Organization, UserOrganization
from datetime import datetime

def create_demo_data():
    """Create demo data for testing"""
    print("Creating demo data...")
    
    # Create demo organization
    demo_org = Organization(
        name='INDOSINT Demo Organization',
        description='Demo organization for testing INDOSINT features',
        domain='demo.indosint.com',
        industry='Technology',
        size='medium',
        subscription_plan='pro'
    )
    db.session.add(demo_org)
    db.session.commit()
    
    # Create demo users
    demo_users = [
        {
            'username': 'admin',
            'email': 'admin@indosint.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'is_verified': True
        },
        {
            'username': 'analyst',
            'email': 'analyst@indosint.com',
            'password': 'analyst123',
            'first_name': 'Analyst',
            'last_name': 'User',
            'role': 'analyst',
            'is_verified': True
        },
        {
            'username': 'user',
            'email': 'user@indosint.com',
            'password': 'user123',
            'first_name': 'Regular',
            'last_name': 'User',
            'role': 'user',
            'is_verified': True
        }
    ]
    
    for user_data in demo_users:
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        
        # Add user to demo organization
        user_org = UserOrganization(
            user_id=user.id,
            organization_id=demo_org.id,
            role='member' if user.role == 'user' else user.role
        )
        db.session.add(user_org)
    
    db.session.commit()
    print("Demo data created successfully!")
    print("\nDemo Accounts:")
    print("Admin: admin@indosint.com / admin123")
    print("Analyst: analyst@indosint.com / analyst123")
    print("User: user@indosint.com / user123")

def init_database():
    """Initialize the database"""
    print("Initializing database...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if demo data exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            create_demo_data()
        else:
            print("Demo data already exists!")

def main():
    """Main application entry point"""
    global app
    
    # Create Flask application
    app = create_app()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init-db':
            init_database()
        elif command == 'create-demo':
            with app.app_context():
                create_demo_data()
        elif command == 'run':
            # Run the application
            print("Starting INDOSINT Application...")
            print("Backend API: http://localhost:5000")
            print("Frontend: http://localhost:3000")
            print("Health Check: http://localhost:5000/health")
            print("\nPress Ctrl+C to stop the server")
            
            app.run(
                host='0.0.0.0',
                port=5000,
                debug=True,
                threaded=True
            )
        else:
            print(f"Unknown command: {command}")
            print("Available commands:")
            print("  init-db     - Initialize database and create demo data")
            print("  create-demo - Create demo data only")
            print("  run         - Run the application")
    else:
        # Default: run the application
        print("Starting INDOSINT Application...")
        print("Backend API: http://localhost:5000")
        print("Frontend: http://localhost:3000")
        print("Health Check: http://localhost:5000/health")
        print("\nPress Ctrl+C to stop the server")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True
        )

if __name__ == '__main__':
    main() 