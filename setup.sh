#!/bin/bash

# INDOSINT - AI-Powered OSINT System Setup Script
# This script sets up the complete INDOSINT system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Docker
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Node.js
    if ! command_exists node; then
        print_error "Node.js is not installed. Please install Node.js 16+ first."
        exit 1
    fi
    
    # Check Python
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.9+ first."
        exit 1
    fi
    
    print_success "System requirements check passed!"
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p backend/logs
    mkdir -p backend/uploads
    mkdir -p backend/ml_models
    mkdir -p backend/nlp_models
    mkdir -p backend/data
    mkdir -p frontend/public
    mkdir -p docs
    mkdir -p scripts
    
    print_success "Directories created successfully!"
}

# Function to setup environment file
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f .env ]; then
        cp env.example .env
        print_warning "Environment file created from template. Please edit .env with your actual configuration."
    else
        print_warning "Environment file already exists. Skipping creation."
    fi
}

# Function to setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Install spaCy models
    print_status "Installing spaCy language models..."
    python -m spacy download en_core_web_sm
    python -m spacy download hi_core_news_sm
    
    # Download NLTK data
    print_status "Downloading NLTK data..."
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
    
    cd ..
    print_success "Backend setup completed!"
}

# Function to setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install Node.js dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    cd ..
    print_success "Frontend setup completed!"
}

# Function to setup databases
setup_databases() {
    print_status "Setting up databases with Docker..."
    
    # Start database services
    docker-compose up -d postgres mongodb redis elasticsearch
    
    # Wait for databases to be ready
    print_status "Waiting for databases to be ready..."
    sleep 30
    
    # Run database migrations
    print_status "Running database migrations..."
    docker-compose exec backend alembic upgrade head
    
    print_success "Database setup completed!"
}

# Function to build and start services
start_services() {
    print_status "Building and starting services..."
    
    # Build and start all services
    docker-compose up -d --build
    
    print_success "Services started successfully!"
}

# Function to run health checks
health_check() {
    print_status "Running health checks..."
    
    # Wait for services to be ready
    sleep 60
    
    # Check backend health
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        print_success "Backend is healthy!"
    else
        print_error "Backend health check failed!"
    fi
    
    # Check frontend health
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        print_success "Frontend is healthy!"
    else
        print_error "Frontend health check failed!"
    fi
    
    # Check database connections
    if docker-compose exec backend python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())" >/dev/null 2>&1; then
        print_success "Database connections are healthy!"
    else
        print_error "Database health check failed!"
    fi
}

# Function to create initial admin user
create_admin_user() {
    print_status "Creating initial admin user..."
    
    # This will be handled by the application on first run
    print_warning "Please create an admin user through the web interface after the system is running."
}

# Function to display setup completion message
display_completion() {
    echo ""
    echo "=========================================="
    echo "🎉 INDOSINT Setup Completed Successfully! 🎉"
    echo "=========================================="
    echo ""
    echo "🌐 Access Points:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo ""
    echo "📊 Monitoring:"
    echo "   Elasticsearch: http://localhost:9200"
    echo "   Redis: localhost:6379"
    echo "   PostgreSQL: localhost:5432"
    echo "   MongoDB: localhost:27017"
    echo ""
    echo "🔧 Management Commands:"
    echo "   Start services: docker-compose up -d"
    echo "   Stop services: docker-compose down"
    echo "   View logs: docker-compose logs -f"
    echo "   Restart services: docker-compose restart"
    echo ""
    echo "📝 Next Steps:"
    echo "   1. Edit .env file with your API keys and configuration"
    echo "   2. Access the frontend at http://localhost:3000"
    echo "   3. Create your first admin user account"
    echo "   4. Configure data sources and API keys"
    echo "   5. Start your first OSINT investigation!"
    echo ""
    echo "📚 Documentation:"
    echo "   Check the docs/ directory for detailed documentation"
    echo "   Visit the API docs at http://localhost:8000/docs"
    echo ""
    echo "⚠️  Important Security Notes:"
    echo "   - Change default passwords in production"
    echo "   - Configure proper SSL/TLS certificates"
    echo "   - Set up proper firewall rules"
    echo "   - Regularly update dependencies"
    echo ""
}

# Main setup function
main() {
    echo "=========================================="
    echo "🚀 INDOSINT - AI-Powered OSINT System"
    echo "=========================================="
    echo ""
    
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_error "Please do not run this script as root!"
        exit 1
    fi
    
    # Check requirements
    check_requirements
    
    # Create directories
    create_directories
    
    # Setup environment
    setup_environment
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    # Setup databases
    setup_databases
    
    # Start services
    start_services
    
    # Run health checks
    health_check
    
    # Create admin user
    create_admin_user
    
    # Display completion message
    display_completion
}

# Function to cleanup on error
cleanup() {
    print_error "Setup failed! Cleaning up..."
    docker-compose down -v 2>/dev/null || true
    exit 1
}

# Set trap for cleanup
trap cleanup ERR

# Run main function
main "$@" 